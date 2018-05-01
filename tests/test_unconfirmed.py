"""Unconfirmed transaction tests"""

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

from minimalcryptocurrency import OutputTransaction
from minimalcryptocurrency import Transaction
from minimalcryptocurrency import UnspentList
from minimalcryptocurrency import UnspentTransaction
from minimalcryptocurrency import Wallet


def test_unconfirmed():
    """Test operation with wallets"""

    wallet_1 = Wallet('aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518')
    wallet_2 = Wallet('7d6433bcc63f973580dc7562d2ca79fcb12bb4e08c7e7333')

    # List of unspent transactions
    unspent = UnspentList()

    # Assign 250 coins to the wallet #1
    unspent.unspent.append(UnspentTransaction('d749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4',
                                              0, wallet_1.get_account(), 250))

    assert unspent.address_amount(wallet_1.get_account()) == 250
    assert unspent.address_amount(wallet_2.get_account()) == 0

    # Link unspent to the wallets
    wallet_1.unspent = unspent
    wallet_2.unspent = unspent

    # Validate accounts
    assert wallet_1.get_balance() == 250
    assert wallet_2.get_balance() == 0

    # Try to transfer 900 coins form 1 to 2
    assert wallet_1.generate_transaction_to(wallet_2.get_account(), 900) is None

    # Generate a transfer of 200 coins form 1 to 2
    transaction = wallet_1.generate_transaction_to(wallet_2.get_account(), 200)

    # The operation can be append to the unconfirmed transactions
    assert unspent.append_unconfirmed(transaction)

    # Cannot add to the unconfirmed list again
    assert unspent.append_unconfirmed(transaction) is False

    # Validate accounts (unconfirmed cannot be spend again)
    assert wallet_1.get_balance() == 0
    assert wallet_2.get_balance() == 0

    # Confirm unconfirmed transactions
    assert unspent.confirm_unconfirmed()

    # Validate accounts
    assert wallet_1.get_balance() == 50
    assert wallet_2.get_balance() == 200

    # Spend more transactions
    assert unspent.append_unconfirmed(wallet_1.generate_transaction_to(wallet_2.get_account(), 25))
    assert unspent.append_unconfirmed(wallet_2.generate_transaction_to(wallet_1.get_account(), 10))
    assert unspent.confirm_unconfirmed()

    # Validate accounts
    assert wallet_1.get_balance() == 35
    assert wallet_2.get_balance() == 215


def test_unconfirmed_minner():
    """Test operation with wallets"""

    # List of unspent transactions
    unspent = UnspentList()

    # Wallets
    wallet_1 = Wallet('aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518')
    wallet_2 = Wallet('7d6433bcc63f973580dc7562d2ca79fcb12bb4e08c7e7333')
    wallet_3 = Wallet('3d66f0ea52a2c5cf42893560d5522e82621790edeb7f609b')

    # Link unspent to the wallets
    wallet_1.unspent = unspent
    wallet_2.unspent = unspent

    assert wallet_1.get_balance() == 0
    assert wallet_2.get_balance() == 0

    # Add transaction for miner
    inputs = datetime(2000, 1, 1, 0, 0, 0)
    outputs = OutputTransaction(wallet_1.public, 5)
    transaction = Transaction(inputs, outputs, wallet_1.private)

    assert unspent.append_unconfirmed(transaction)
    assert unspent.append_unconfirmed(transaction) is False

    assert unspent.confirm_unconfirmed()
    assert wallet_1.get_balance() == 5
    assert wallet_2.get_balance() == 0
