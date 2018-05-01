"""Tests for the Wallet object"""

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

from minimalcryptocurrency import UnspentList
from minimalcryptocurrency import UnspentTransaction
from minimalcryptocurrency import Wallet
from minimalcryptocurrency import generate_public_key


def test_wallet_creation():
    """Test Wallet creation"""

    wallet = Wallet()

    assert wallet.public == generate_public_key(wallet.private)


def test_wallet_from_key():
    """Test Wallet creation from a key"""

    wallet = Wallet('aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518')

    assert wallet.account == \
           '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c'

    assert wallet.public == \
           '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c'

    assert wallet.private == \
           'aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518'

    assert wallet.key == \
           'aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518'

    assert wallet.get_account() == wallet.public

    assert repr(wallet) == \
           '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c (0)'


def test_wallet_operation():
    """Test operation with wallets"""

    wallet_1 = Wallet('aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518')
    wallet_2 = Wallet('7d6433bcc63f973580dc7562d2ca79fcb12bb4e08c7e7333')
    wallet_3 = Wallet('3d66f0ea52a2c5cf42893560d5522e82621790edeb7f609b')

    # List of unspent transactions
    unspent = UnspentList()

    # Assign 100 coins to the wallet #1
    unspent.unspent.append(UnspentTransaction('d749929fe94b9a37dbe5d74cb297ad24b46e467898545f4e109eb21835046ac4',
                                              0, wallet_1.get_account(), 100))

    assert unspent.address_amount(wallet_1.get_account()) == 100
    assert unspent.address_amount(wallet_2.get_account()) == 0
    assert unspent.address_amount(wallet_3.get_account()) == 0

    # Link unspent to the wallets
    wallet_1.unspent = unspent
    wallet_2.unspent = unspent
    wallet_3.unspent = unspent

    # Validate accounts
    assert wallet_1.get_balance() == 100
    assert wallet_2.get_balance() == 0
    assert wallet_3.get_balance() == 0

    # Try to transfer 900 coins form 1 to 2
    assert wallet_1.generate_transaction_to(wallet_2.get_account(), 900) is None

    # Transfer 90 coins form 1 to 2
    transaction = wallet_1.generate_transaction_to(wallet_2.get_account(), 90)

    assert transaction is not None
    assert transaction.hash_id == transaction.generate_transaction_id()

    # Spend the transaction
    assert unspent.validate_transaction(transaction)
    assert unspent.spend_transaction(transaction)
    assert unspent.validate_transaction(transaction) is False

    assert wallet_1.get_balance() == 10
    assert wallet_2.get_balance() == 90
    assert wallet_3.get_balance() == 0

    # Transfer 50 form 1 to 3
    assert wallet_1.transfer_to(wallet_3.get_account(), 50) is False

    # Transfer 5 form 1 to 3
    assert wallet_1.transfer_to(wallet_3.get_account(), 5)

    assert wallet_1.get_balance() == 5
    assert wallet_2.get_balance() == 90
    assert wallet_3.get_balance() == 5

    # Transfer 0.5 form 2 to 3
    assert wallet_2.transfer_to(wallet_3.get_account(), 0.5)

    assert wallet_1.get_balance() == 5
    assert wallet_2.get_balance() == 89.5
    assert wallet_3.get_balance() == 5.5
