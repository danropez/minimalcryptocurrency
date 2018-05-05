"""Transaction"""

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

from ecdsa import SigningKey

from minimalcryptocurrency import is_signature_valid


class InputTransaction:
    """Input transaction class"""

    def __init__(self, hash_id, index):
        """Create a new UnspentTransaction Object

        Args:
            hash_id (String): the transaction id
            index (Integer): the index in the transaction id
        """

        self.hash_id = hash_id
        self.index = index

    def __eq__(self, transaction):
        """ Return self==value. """

        return self.hash_id == transaction.hash_id and \
               self.index == transaction.index

    def __repr__(self):
        """ Return repr(self). """

        return "%s (%d)" % (self.hash_id, self.index)


class OutputTransaction:
    """Output transaction class"""

    def __init__(self, address, amount):
        """Create a new UnspentTransaction Object

        Args:
            address (String): the owner address
            amount (Double): the amount of currency in the transaction
        """

        self.address = address
        self.amount = amount

    def __repr__(self):
        """ Return repr(self). """

        return "%s (%d)" % (self.address, self.amount)


class Transaction:
    """Transaction class"""

    def __init__(self, inputs, outputs=None, key=None):
        """Create a new UnspentTransaction Object

        Args:
            inputs (Array): list of input transaction to be spend
            outputs (Array): list of output transaction to be generated
            key (String): private key to sign the transaction
        """

        if isinstance(inputs, InputTransaction):
            self.inputs = [inputs]
        else:
            self.inputs = inputs

        if isinstance(outputs, OutputTransaction):
            self.outputs = [outputs]
        else:
            self.outputs = outputs

        self.hash_id = self.generate_transaction_id()

        if key is None:
            self.signature = ''
        else:
            self.sign(key)

    def generate_transaction_id(self):
        """Calculate the id of the transaction

        Returns:
            (String): the transaction id
        """

        transaction = []

        for outputs in self.outputs:
            transaction.append(outputs.address)
            transaction.append(outputs.amount)

        if self.inputs is not None:
            if isinstance(self.inputs, datetime):
                transaction.append('%s' % self.inputs)
            else:
                for inputs in self.inputs:
                    if isinstance(inputs, InputTransaction):
                        transaction.append(inputs.hash_id)
                    else:
                        transaction.append(inputs)

        return sha256(repr(transaction).encode('utf-8')).hexdigest()

    def sign(self, key):
        """Sign the operation

        Args:
            key (String): the private key of the owner

        Returns:
            (String): the signature of the transaction
        """

        signature_key = SigningKey.from_string(bytes.fromhex(key))
        self.signature = signature_key.sign(self.hash_id.encode('utf-8')).hex()


class UnspentList:
    """List of unspent transaction class"""

    def __init__(self):
        """Create a new UnspentList Object"""

        # List of unspent transactions
        self.unspent = []

        # List of new transactions to be spend
        self.unconfirmed = []

    def __spend(self, transaction):
        """Spend the transaction"""

        use_transactions = []

        # Validate input transaction
        if not isinstance(transaction.inputs, datetime):
            for inputs in transaction.inputs:
                for unspent in self.unspent:
                    if unspent.hash_id == inputs.hash_id and \
                            unspent.index == inputs.index:
                        use_transactions.append(unspent)

        # Spend all transactions
        for unspent in use_transactions:
            self.unspent.remove(unspent)

        # Create the new transaction
        for index in range(len(transaction.outputs)):
            unspent = UnspentTransaction(transaction.hash_id, index,
                                         transaction.outputs[index].address,
                                         transaction.outputs[index].amount)

            self.unspent.append(unspent)

    def address_amount(self, address):
        """Calculate total unspent amount for an account

        Get all unspent transactions and get the total amount in this account

        Args:
            address (String): an address

        Returns:
            (Double): the total amount in the address
        """

        amount = 0

        transactions = self.address_transactions(address)

        for transaction in transactions:
            amount += transaction.amount

        return amount

    def address_transactions(self, address):
        """Get all unspent transactions for an account

        Args:
            address (String): an address

        Returns:
            (Array): an array of unspent transactions
        """

        result = []

        for unspent in self.unspent:
            if unspent.address == address:
                result.append(unspent)

        # Remove unconfirmed from the results
        for unconfirmed in self.unconfirmed:
            if not isinstance(unconfirmed.inputs, datetime):
                for unconfirmed_inputs in unconfirmed.inputs:
                    for unspent in result:
                        if unconfirmed_inputs.index == unspent.index and \
                                unconfirmed_inputs.hash_id == unspent.hash_id:
                            result.remove(unspent)

        return result

    def append_unconfirmed(self, transaction):
        """Append and uncofrimed trasaction

        Args:
            transaction (Transaction): an transaction object

        Returns:
            (Boolean): True is the transaction can been append to the unconfirmed list
        """
        if self.validate_transaction(transaction):
            self.unconfirmed.append(transaction)
            return True

        return False

    def confirm_unconfirmed(self):
        """Confirm the list of unconfirmed transactions"""

        for unconfirmed in self.unconfirmed:
            self.__spend(unconfirmed)

        self.unconfirmed = []

        return True

    def spend_transaction(self, transaction):
        """Spend a transaction

        Spend the transactions and create new unspent transactions

        Args:
            transaction (Transaction): an transaction object

        Returns:
            (Boolean): True is the transaction has been spent
        """

        if self.validate_transaction(transaction):
            self.__spend(transaction)

            # Finish the spend
            return True

        return False

    def validate_transaction(self, transaction):
        """Validate a transaction

        Args:
            transaction (Transaction): an transaction object

        Returns:
            (Boolean): True is the transaction can been spent
        """

        # Validata input transaction is valid
        if not isinstance(transaction, Transaction):
            return False

        use_transactions = []
        need_validation = True

        # Validate input transaction
        if transaction.inputs is None or isinstance(transaction.inputs, datetime):
            need_validation = False

            for unconfirmed in self.unconfirmed:
                for unconfirmed_outputs in unconfirmed.outputs:
                    for outputs in transaction.outputs:
                        if unconfirmed_outputs == outputs:
                            return False
        else:
            for inputs in transaction.inputs:
                for unspent in self.unspent:
                    # validata that the transaction is not on the unconfirmed
                    for unconfirmed in self.unconfirmed:
                        for unconfirmed_inputs in unconfirmed.inputs:
                            if unconfirmed_inputs == inputs:
                                return False

                    # Validate the signature
                    if unspent.hash_id == inputs.hash_id and \
                            unspent.index == inputs.index:
                        if is_signature_valid(transaction.hash_id,
                                              transaction.signature, unspent.address):
                            use_transactions.append(unspent)
                        else:
                            return False

        # Validate the number of transactions
        if need_validation and len(transaction.inputs) != len(use_transactions):
            return False

        # Input and output amount are the same
        total_in = 0
        total_out = 0

        for unspent in use_transactions:
            total_in += unspent.amount

        for output in transaction.outputs:
            total_out += output.amount

        if need_validation and total_in != total_out:
            return False

        # Finish the validation
        return True


class UnspentTransaction:
    """Unspent transactions class"""

    def __init__(self, hash_id, index, address, amount):
        """Create a new UnspentTransaction Object

        Args:
            hash_id (String): the transaction id
            index (Integer): the index in the transaction id
            address (String): the owner address
            amount (Double): the amount of currency in the transaction
        """

        self.hash_id = hash_id
        self.index = index
        self.address = address
        self.amount = amount

    def __eq__(self, other):
        """ Return self==value. """

        if self.hash_id == other.hash_id and self.index == other.index:
            return True

        return False
