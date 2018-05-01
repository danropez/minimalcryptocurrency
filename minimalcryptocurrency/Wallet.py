"""Wallet"""

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

from ecdsa import SigningKey

from minimalcryptocurrency import InputTransaction
from minimalcryptocurrency import OutputTransaction
from minimalcryptocurrency import Transaction
from minimalcryptocurrency import generate_public_key


class Wallet:
    """Wallet class """

    def __init__(self, private=None, blockchain=None):
        """Generate a new Wallet

        Generate a new Wallet using a private key of from zero

        Args:
            private (String): the private key for the wallet. Where it is not
                              indicate it will generate a new pair.
            blockchain (Blockchain): an object with the blockchain
        """

        if private is None:
            sk = SigningKey.generate()
            self.private = sk.to_string().hex()
            self.public = sk.get_verifying_key().to_string().hex()
        else:
            self.private = private
            self.public = generate_public_key(private)

        self.unspent = None
        self.blockchain = blockchain

    def __repr__(self):
        """ Return repr(self). """

        return "%s (%d)" % (self.public, self.get_balance())

    def __update_unspent(self):
        if self.blockchain is not None:
            self.unspent = self.blockchain.get_unspent_list()

    @property
    def account(self):
        """Get the user account"""

        return self.public

    def generate_transaction_to(self, account, amount):
        """Generate the transactions to an account

        Args:
            account (String): the destination account
            amount (Double): the amount to transfer

        Returns:
            (Transaction): a signed transaction where it is possible, None otherwise.
        """

        # Update unspent list
        self.__update_unspent()

        # Validate if there are enough balance
        if self.get_balance() < amount:
            return None

        # Get the unspent transaction
        user_transactions = self.unspent.address_transactions(self.public)

        # Generate the input accounts
        inputs = []
        used_from_balance = 0

        for transaction in user_transactions:
            used_from_balance += transaction.amount
            inputs.append(InputTransaction(transaction.hash_id, transaction.index))

            if used_from_balance >= amount:
                break

        # Calculate the quantity to keep in balance
        keep_in_balance = used_from_balance - amount

        # Calculate output transfers
        if keep_in_balance == 0:
            outputs = OutputTransaction(account, amount)
        else:
            outputs = [OutputTransaction(account, amount), OutputTransaction(self.public, keep_in_balance)]

        # Generate transaction and sign
        transaction = Transaction(inputs, outputs, self.private)

        return transaction

    def get_account(self):
        """Return the account number

        Returns:
            (String): the account number
        """

        return self.public

    def get_balance(self):
        """Get the balance in the Wallet

        Returns:
            (Double): the total amount in the wallet
        """

        # Update unspent list
        self.__update_unspent()

        if self.unspent is None:
            return 0
        else:
            return self.unspent.address_amount(self.public)

    @property
    def key(self):
        """Get the user key"""

        return self.private

    def transfer_to(self, account, amount):
        """Transfer from the wallet ot another account

        Args:
            account (String): the destination account
            amount (Double): the amount to transfer

        Returns:
            (Boolean): True is the transfer were done.
        """

        # Update unspent list
        self.__update_unspent()

        transaction = self.generate_transaction_to(account, amount)

        if transaction is None:
            return False
        else:
            return self.unspent.spend_transaction(transaction)
