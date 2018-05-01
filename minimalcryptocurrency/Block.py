"""Block"""

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
from hashlib import sha256


class Block:
    """Block object"""

    def __init__(self, index, data, previous_hash=None, timestamp=None, proof=0, difficulty=0):
        """Create a new Block Object

        Create a new Block Object

        Args:
            index (Integer): the index of the block
            data (Object): data store in the block
            previous_hash (String): the hash of previous block
            timestamp (Time): the genesis block time
            proof (Integer): the proof
            difficulty (Integer): the number of zeros in the hash to validate the block
        """

        # Default values for internal properties
        self.__proof = None
        self.hash = None

        # Define basic information about the Block
        if isinstance(index, Block):
            self.index = index.index + 1
            self.previous_hash = index.hash
            self.difficulty = index.difficulty
        else:
            self.index = index
            self.previous_hash = previous_hash
            self.difficulty = difficulty

        # Get actual date or use timestamp
        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp

        # Se the rest of values
        self.data = data
        self.proof = proof

    def __repr__(self):
        """ Return repr(self). """

        return "Block: %d (%s)\n Hash: %s\n Previous: %s" % (
            self.index, self.timestamp, self.hash, self.previous_hash)

    def __eq__(self, block):
        """ Return self==value. """

        result = self.index == block.index
        result = result and self.previous_hash == block.previous_hash
        result = result and self.timestamp == block.timestamp
        result = result and self.data == block.data
        result = result and self.hash == block.hash

        return result

    @property
    def hash_satisfies_difficulty(self):
        """Evaluate if the hash satisfies the difficulty

        Return:
             (Logical): Evaluate if the hash starts with the minimum number of
                        zeros indicated in the ``difficulty`` parameter.
        """

        binary_hash = bin(int(self.hash, 16))[2:].zfill(len(self.hash) * 4)

        return binary_hash[:self.difficulty] == "0" * self.difficulty

    @property
    def is_valid(self):
        """Evaluate if the block is valid

        Return:
             (Logical): True if the block proof value satisfied the required
                        ``difficult``parameter and the hash is valid.
        """

        return self.hash_satisfies_difficulty and self.hash == self.calculate_hash()

    @property
    def proof(self):
        """The proof of work

        The values of the Proof of Work in the block
        """

        return self.__proof

    @proof.setter
    def proof(self, proof):
        """Set the proof of work"""

        self.__proof = proof

        # Calculate hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the hash of a block

        Calculate the hash of a block

        Args:
            self (Block): A Block object
        """

        block = [self.index, self.previous_hash, self.timestamp, self.data, self.proof, self.difficulty]

        return sha256(repr(block).encode('utf-8')).hexdigest()

    @staticmethod
    def genesis_block(data=None, timestamp=None, proof=0, difficulty=0, mining=False):
        """Generate a genesis block

        Args:
            data (Object): the data to store in the block
            timestamp (String): the genesis block time
            proof (Integer): the proof
            difficulty (Integer): the number of zeros in the hash to validate the block
            mining (Boolean): logical value indicating if the block must be mined

        Return:
             A Block
        """

        if timestamp is None:
            hash_id = sha256(''.encode('utf-8')).hexdigest()
        else:
            hash_id = '%s' % timestamp
            hash_id = sha256(hash_id.encode('utf-8')).hexdigest()

        block = Block(0, data, hash_id, timestamp, proof, difficulty)

        if mining:
            while not block.is_valid:
                block.mining()

        return block

    def mining(self, init=None, maximum_iter=1000):
        """Mining the Block

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

        if init is not None:
            self.proof = init

        number_iter = 0

        while not self.is_valid and number_iter < maximum_iter:
            self.proof += 1
            number_iter += 1

        return self.is_valid
