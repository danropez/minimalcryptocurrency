"""Tutorial test"""

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
    """Test basic process of a create a cryptocurrency"""

    # Generate first user
    wallet = Wallet()

    # Create a new currency with 10 units
    blockchain = BlockChain.new_cryptocurrency(wallet.account, 10, timestamp=datetime(2018, 1, 1, 0, 0, 0),
                                               difficulty=4, mining=True)

    # Get the wallets of Alice and Bob
    alice = blockchain.get_wallet(wallet.key)
    bob = blockchain.get_wallet()

    assert alice.get_balance() == 10
    assert bob.get_balance() == 0

    # Alice transfer to Bob 5 units and get 10 units because she mining the block
    assert blockchain.add_transaction(alice.key, bob.account, 5)

    blockchain.generate_candidate(alice.account, timestamp=datetime(2018, 1, 1, 0, 1, 0))
    blockchain.mining_candidate()

    assert alice.get_balance() == 15
    assert bob.get_balance() == 5

    # New users Carol, Dan and Eve
    carol = blockchain.get_wallet()
    dan = blockchain.get_wallet()
    eve = blockchain.get_wallet()

    # Alice transfer 3 to Carol and 4.5 to Dan
    assert blockchain.add_transaction(alice.key, carol.account, 3)
    assert blockchain.add_transaction(alice.key, dan.account, 4.5)

    # Bon transfer 2.2 to Dan
    assert blockchain.add_transaction(bob.key, dan.account, 2.2)

    # Eve mine the Block
    blockchain.generate_candidate(eve.account, timestamp=datetime(2018, 1, 1, 0, 2, 0))
    blockchain.mining_candidate()

    assert alice.get_balance() == 7.5
    assert bob.get_balance() == 2.8
    assert carol.get_balance() == 3
    assert dan.get_balance() == 6.7
    assert eve.get_balance() == 10
