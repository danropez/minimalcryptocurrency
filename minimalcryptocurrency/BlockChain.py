"""BlockChain"""

#
#  Created by Daniel Rodriguez Perez.
#
#  Copyright (c) 2018 Daniel Rodriguez Perez.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#

from datetime import datetime

from minimalcryptocurrency import Block
from minimalcryptocurrency import OutputTransaction
from minimalcryptocurrency import Transaction
from minimalcryptocurrency import UnspentList
from minimalcryptocurrency import Wallet


class BlockChain:
    """BlockChain object"""

    def __init__(self, block=None):
        """BlockChain object"""

        # Difficulty update parameters
        self.minimum_interval = 59  # 59 Seconds - the minimum interval between blocks is a minute
        self.block_interval = 600  # 10 minutes - the objective interval between blocks
        self.difficulty_interval = 144  # 144 block - the time for evaluate intervals (one per day 6 * 24)

        # Currency values
        self.__unspent = None
        self.amount_mining = 0

        # Validate the inputs
        if block is None:
            self.__candidate = Block.genesis_block()
        elif isinstance(block, Block):
            self.__candidate = block
        else:
            raise Exception("The input parameter must be a Block object")

        if self.__candidate.is_valid:
            self.chain = [self.__candidate]
            self.__candidate = None
        else:
            self.chain = []

    def __repr__(self):
        """ Return repr(self). """

        last_block = max(0, len(self.chain) - 5)
        result = ""

        for step in reversed(range(last_block, len(self.chain))):
            result = "%sBlock: %d (%s) - Hash: %s\n" % \
                     (result, self.chain[step].index, self.chain[step].timestamp, self.chain[step].hash)

        if last_block > 0:
            result = '%s\nand %d block hidden' % (result, last_block)

        return result

    @property
    def is_valid(self):
        """Indicate if the blockchain is valid

        The blockchain is valid when
            1) The blocks are valid
            2) All blocks has previous block hash and a valid id
            3) All blocks are valid and

        Return:
             (Logical): True if BlockChain is valid
        """

        if self.chain:
            for step in range(len(self.chain) - 1, 0, -1):
                if not self.chain[step].is_valid:
                    return False
                elif self.chain[step].previous_hash != self.chain[step - 1].hash:
                    return False
                elif self.chain[step].index != self.chain[step - 1].index + 1:
                    return False

            return self.chain[0].is_valid

        return False

    @property
    def candidate_block(self):
        """Return the candidate for block for the chain"""

        return self.__candidate

    @property
    def last_block(self):
        """Return the last block in the BlockChain"""

        if self.chain:
            return self.chain[-1]
        else:
            return None

    @property
    def num_blocks(self):
        """Return the number of blocks in the chain"""

        return len(self.chain)

    def add_candidate(self, data, timestamp=None, proof=0):
        """Insert a new candidate in the chain

        Return:
            (logical): true where the candidate can be assigned
        """

        if self.__candidate is not None:
            return False
        else:
            # Get the timestamp value where it is None
            if timestamp is None:
                timestamp = datetime.now()

            # Validate minimum timestamp period
            interval = timestamp - self.last_block.timestamp
            if interval.total_seconds() < self.minimum_interval:
                return False

            # Evaluate the difficulty
            if len(self.chain) > 0 and len(self.chain) % self.difficulty_interval == 0:
                interval = self.chain[-1].timestamp - self.chain[-self.difficulty_interval].timestamp
                interval = interval.total_seconds() / (self.difficulty_interval - 1)

                if interval > self.block_interval:
                    difficulty = self.last_block.difficulty - 1
                elif interval < self.block_interval:
                    difficulty = self.last_block.difficulty + 1

            else:
                difficulty = self.last_block.difficulty

            self.__candidate = Block(self.last_block.index + 1, data, previous_hash=self.last_block.hash,
                                     timestamp=timestamp, proof=proof, difficulty=difficulty)

            return True

    def add_transaction(self, key, address, amount):
        """Add a transaction in the blockchain

        Add a transaction to the candidate list from the signer's account to the destination account for the indicated
        amount.

        Args:
            key (String): the private key of the user
            address (String): the destination address
            amount (Double): the amount of the

        Return:
            (Boolean): True if the transaction can be done
        """
        wallet = self.get_wallet(key)
        transaction = wallet.generate_transaction_to(address, amount)

        if transaction is None:
            return False

        unspent = self.get_unspent_list()

        return unspent.append_unconfirmed(transaction)

    def candidate_proof(self, proof):
        """Set the proof for a candidate"""

        self.__candidate.proof = proof

        if self.__candidate.is_valid:
            self.chain.append(self.__candidate)
            self.__candidate = None
            self.__unspent = None
            return True

        return False

    def generate_candidate(self, address, timestamp=None, proof=0):
        """Generate a new candidate block with a reward to the miner

        Args:
            address (String): the address fo the miner
            timestamp (String): the genesis block time
            proof (Integer): the proof

        Return:
            (logical): true where the candidate can be assigned
        """

        output = OutputTransaction(address, self.amount_mining)
        transaction = Transaction(timestamp, output)

        self.__unspent.append_unconfirmed(transaction)
        data = self.__unspent.unconfirmed

        return self.add_candidate(data, timestamp=timestamp, proof=proof)

    def get_unspent_list(self):
        """Get the list of unspent transaction

        Return:
            (UnspentList): the list unspent transactions
        """

        if self.__unspent is None:
            self.__unspent = UnspentList()

            for block in self.chain:
                for transaction in block.data:
                    assert self.__unspent.append_unconfirmed(transaction)

                if block.is_valid:
                    self.__unspent.confirm_unconfirmed()

        return self.__unspent

    def get_wallet(self, key=None):
        """Get the wallet of a user

        Args:
            key (String): the private key of the user

        Return:
             (Wallet): the wallet of the user
        """

        return Wallet(key, self)

    def mining_candidate(self, init=None, maximum_iter=1000):
        """Mining the Candidate Block

        Implements the search of an integer for the proof which satisficed the
        required difficult. The initial value can be configured using the
        `init` property. The maximum number of values to tried can be also
        configured using the `init` property.

        Args:
            self (Block): A Block object
            init (Integer): The values to use in the first proof
            maximum_iter (Integer): The maximum number of iterations in the mining process

        Return:
             (Logical): True if a valid proof has been found
        """

        if self.__candidate.mining(init, maximum_iter):
            self.chain.append(self.__candidate)
            self.__candidate = None
            self.__unspent = None
            return True

        return False

    @staticmethod
    def new_cryptocurrency(address, amount, timestamp=None, proof=0, difficulty=0, mining=False):
        """Create a new cryptocurrency

        Args:
            address (string): the address of the first user
            amount (Double): the amount for the first user
            timestamp (String): the genesis block time
            proof (Integer): the proof
            difficulty (Integer): the number of zeros in the hash to validate the block
            mining (Boolean): logical value indicating if the block must be mined

        Return:
            (BlockChain): A new blockchain
        """

        output = OutputTransaction(address, amount)
        transaction = Transaction(timestamp, output)
        block = Block.genesis_block([transaction], timestamp=timestamp, proof=proof, difficulty=difficulty,
                                    mining=mining)

        blokchain = BlockChain(block)
        blokchain.amount_mining = amount

        return blokchain

    def replace_chain(self, new_chain):
        """Replace this chair for a longest one

        Return:
            (logical): True is the replacement is valid
        """

        if isinstance(new_chain, BlockChain):
            if new_chain.num_blocks > self.num_blocks:
                if new_chain.chain[0] == self.chain[0]:
                    if new_chain.is_valid:
                        self.chain = new_chain.chain
                        self.__candidate = new_chain.candidate_block

                        return True

        return False
