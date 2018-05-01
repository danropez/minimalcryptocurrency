"""Tests for the Transaction object"""

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

from minimalcryptocurrency import InputTransaction
from minimalcryptocurrency import OutputTransaction
from minimalcryptocurrency import Transaction
from minimalcryptocurrency import UnspentList
from minimalcryptocurrency import UnspentTransaction
from minimalcryptocurrency import generate_public_key
from minimalcryptocurrency import is_signature_valid


def test_input_transaction():
    """Test InputTransaction class"""

    input_transaction = InputTransaction('d749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4', 0)

    assert repr(input_transaction) == 'd749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4 (0)'


def test_output_transaction():
    """Test OutputTransaction class"""

    public = generate_public_key('aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518')
    output = OutputTransaction(public, 10)

    assert repr(output) == \
           '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c (10)'


def test_unspent_transaction():
    """Test UnspentTransaction class"""

    account = generate_public_key('aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518')

    unspent = UnspentTransaction('d749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4', 5, account, 12)

    assert unspent.hash_id == 'd749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4'
    assert unspent.index == 5
    assert unspent.address == account
    assert unspent.amount == 12


def test_basic_transaction():
    """"Test basic transactions"""

    # List of users accounts
    private_1 = 'aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518'
    private_2 = '7d6433bcc63f973580dc7562d2ca79fcb12bb4e08c7e7333'
    private_3 = '3d66f0ea52a2c5cf42893560d5522e82621790edeb7f609b'

    public_1 = generate_public_key(private_1)
    public_2 = generate_public_key(private_2)
    public_3 = generate_public_key(private_3)

    # List of unspent transactions
    unspent = UnspentList()

    # Assign 10 coins to user 1
    unspent.unspent.append(
        UnspentTransaction('d749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4', 0, public_1, 10))

    # Assign 10 coins to user 2
    unspent.unspent.append(
        UnspentTransaction('fa34b15a4eb8e91ebeff64edba51d21905e1ac8ce2bff8865da08055bced0dd4', 0, public_2, 10))

    # Validate users amount
    assert unspent.address_amount(public_1) == 10
    assert unspent.address_amount(public_2) == 10
    assert unspent.address_amount(public_3) == 0

    # Move 10 coins from account 1 to account 3
    transaction_input = InputTransaction('d749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4', 0)
    transaction_output = OutputTransaction(public_3, 10)
    transaction = Transaction(transaction_input, transaction_output)

    # The transaction is no signed
    assert is_signature_valid(transaction.hash_id, transaction.signature, public_1) is False
    assert unspent.validate_transaction(transaction) is False
    assert unspent.spend_transaction(transaction) is False

    # The transaction is signed by user 3
    transaction.sign(private_3)

    assert is_signature_valid(transaction.hash_id, transaction.signature, public_1) is False
    assert is_signature_valid(transaction.hash_id, transaction.signature, public_3)
    assert unspent.validate_transaction(transaction) is False
    assert unspent.spend_transaction(transaction) is False

    # The transaction is signed by user 1
    transaction.sign(private_1)

    assert is_signature_valid(transaction.hash_id, transaction.signature, public_1)
    assert unspent.validate_transaction(transaction)
    assert unspent.spend_transaction(transaction)
    assert unspent.validate_transaction(transaction) is False

    # Validate users amount
    assert unspent.address_amount(public_1) == 0
    assert unspent.address_amount(public_2) == 10
    assert unspent.address_amount(public_3) == 10


def test_multiple_transaction():
    """"Test multiple transactions"""

    # List of users accounts
    private_1 = 'aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518'
    private_2 = '7d6433bcc63f973580dc7562d2ca79fcb12bb4e08c7e7333'
    private_3 = '3d66f0ea52a2c5cf42893560d5522e82621790edeb7f609b'

    public_1 = generate_public_key(private_1)
    public_2 = generate_public_key(private_2)
    public_3 = generate_public_key(private_3)

    # List of unspent transactions
    unspent = UnspentList()

    # Assign 10 coins to user 1
    unspent.unspent.append(
        UnspentTransaction('d749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4', 0, public_1, 10))

    # Assign 10 coins to user 2
    unspent.unspent.append(
        UnspentTransaction('fa34b15a4eb8e91ebeff64edba51d21905e1ac8ce2bff8865da08055bced0dd4', 0, public_2, 10))

    # Validate users amount
    assert unspent.address_amount(public_1) == 10
    assert unspent.address_amount(public_2) == 10
    assert unspent.address_amount(public_3) == 0

    # Cannot validate None transactions
    assert unspent.validate_transaction(None) is False
    assert unspent.spend_transaction(None) is False

    # Cannot validate other validations
    assert unspent.validate_transaction('transactions') is False
    assert unspent.spend_transaction('transactions') is False

    # Account 1 move 5 to account 2
    input = InputTransaction('d749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4', 0)
    output = OutputTransaction(public_3, 5)
    transaction = Transaction(input, output)

    # The transaction is no signed
    assert is_signature_valid(transaction.hash_id, transaction.signature, public_1) is False
    assert unspent.validate_transaction(transaction) is False
    assert unspent.spend_transaction(transaction) is False

    # The transaction is signed by user 2
    transaction.sign(private_2)

    assert is_signature_valid(transaction.hash_id, transaction.signature, public_1) is False
    assert is_signature_valid(transaction.hash_id, transaction.signature, public_2)
    assert unspent.validate_transaction(transaction) is False
    assert unspent.spend_transaction(transaction) is False

    # The transaction is signed by user 1
    transaction.sign(private_1)

    # The transaction is not valid because he don't spend all currencies
    assert is_signature_valid(transaction.hash_id, transaction.signature, public_1)
    assert unspent.validate_transaction(transaction) is False
    assert unspent.spend_transaction(transaction) is False

    # Account 1 move 5 to account 2 ans 5 to himself
    input = InputTransaction('d749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4', 0)
    output = [OutputTransaction(public_1, 5), OutputTransaction(public_2, 5)]
    transaction = Transaction(input, output)

    # The transaction is signed by user 1
    transaction.sign(private_1)

    # The transaction is valid and can be spend
    assert is_signature_valid(transaction.hash_id, transaction.signature, public_1)
    assert unspent.validate_transaction(transaction)
    assert unspent.spend_transaction(transaction)
    assert unspent.validate_transaction(transaction) is False

    # Validate users amount
    assert unspent.address_amount(public_1) == 5
    assert unspent.address_amount(public_2) == 15
    assert unspent.address_amount(public_3) == 0

    # User 2 move 12 coins to 3 and 3 to himself
    user_transactions = unspent.address_transactions(public_2)
    input_transactions = []

    for user in user_transactions:
        input_transactions.append(InputTransaction(user.hash_id, user.index))

    output = [OutputTransaction(public_2, 3), OutputTransaction(public_3, 12)]
    transaction = Transaction(input_transactions, output)

    # The transaction is signed by user 2
    transaction.sign(private_2)

    # The transaction is valid and can be spend
    assert is_signature_valid(transaction.hash_id, transaction.signature, public_2)
    assert unspent.validate_transaction(transaction)
    assert unspent.spend_transaction(transaction)
    assert unspent.validate_transaction(transaction) is False

    assert unspent.address_amount(public_1) == 5
    assert unspent.address_amount(public_2) == 3
    assert unspent.address_amount(public_3) == 12

    # User 3 spend 3 in 1 and 2
    input_transactions = []
    user_transactions = unspent.address_transactions(public_3)

    for user in user_transactions:
        input_transactions.append(InputTransaction(user.hash_id, user.index))

    output = [OutputTransaction(public_1, 3), OutputTransaction(public_2, 3), OutputTransaction(public_3, 6)]
    transaction = Transaction(input_transactions, output)

    # The transaction is signed by user 3
    transaction.sign(private_3)

    # The transaction is valid and can be spend
    assert is_signature_valid(transaction.hash_id, transaction.signature, public_3)
    assert unspent.validate_transaction(transaction)
    assert unspent.spend_transaction(transaction)
    assert unspent.validate_transaction(transaction) is False

    assert unspent.address_amount(public_1) == 8
    assert unspent.address_amount(public_2) == 6
    assert unspent.address_amount(public_3) == 6
