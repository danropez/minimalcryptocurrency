"""Minimal Cryptocurrency operation test"""

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

from minimalcryptocurrency import BlockChain
from minimalcryptocurrency import Wallet

def test_minimal_cryptocurrency():
    """Test the operation with a minimal cryptocurrency"""

    wallet_1 = Wallet('aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518')

    # Launch a new currency
    blockchain = BlockChain.new_cryptocurrency(wallet_1.public, 100,timestamp=datetime(2000, 1, 1, 0, 0, 0),
                                               difficulty=4, mining=True)

    # Open the wallets
    wallet_1 = blockchain.get_wallet('aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518')
    wallet_2 = blockchain.get_wallet('7d6433bcc63f973580dc7562d2ca79fcb12bb4e08c7e7333')
    wallet_3 = blockchain.get_wallet('3d66f0ea52a2c5cf42893560d5522e82621790edeb7f609b')

    # Ask for the accounts
    assert wallet_1.get_balance() == 100
    assert wallet_2.get_balance() == 0
    assert wallet_3.get_balance() == 0

    # Generate an unspent transaction
    assert blockchain.add_transaction(wallet_1.private, wallet_2.public, 190) is False
    assert blockchain.add_transaction(wallet_1.private, wallet_2.public, 90)
    assert blockchain.add_transaction(wallet_1.private, wallet_2.public, 90) is False

    # Generate a candidate to mining
    blockchain.generate_candidate(wallet_1.public, timestamp=datetime(2000, 1, 1, 0, 1, 0))
    blockchain.mining_candidate()

    # Ask for the accounts
    assert wallet_1.get_balance() == 110
    assert wallet_2.get_balance() == 90
    assert wallet_3.get_balance() == 0

    # Move more operations
    assert blockchain.add_transaction(wallet_1.private, wallet_2.public, 10)
    assert blockchain.add_transaction(wallet_2.private, wallet_3.public, 20)

    # Generate a candidate to mining
    blockchain.generate_candidate(wallet_1.public, timestamp=datetime(2000, 1, 1, 0, 2, 0))
    blockchain.mining_candidate()

    # Ask for the accounts
    assert wallet_1.get_balance() == 200
    assert wallet_2.get_balance() == 80
    assert wallet_3.get_balance() == 20

    # Move more operations
    assert blockchain.add_transaction(wallet_1.private, wallet_2.public, 25)
    assert blockchain.add_transaction(wallet_1.private, wallet_3.public, 25)
    assert blockchain.add_transaction(wallet_2.private, wallet_3.public, 50)

    # Generate a candidate to mining
    blockchain.generate_candidate(wallet_2.public, timestamp=datetime(2000, 1, 1, 0, 3, 0))
    blockchain.mining_candidate()

    # Ask for the accounts
    assert wallet_1.get_balance() == 150
    assert wallet_2.get_balance() == 155
    assert wallet_3.get_balance() == 95
