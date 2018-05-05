"""Tests for the Blockchain object"""

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

import pytest

from minimalcryptocurrency import Block
from minimalcryptocurrency import BlockChain


def test_creation_blockchain():
    """Test errors during the build of an object"""

    # The input is not a block object
    with pytest.raises(Exception):
        BlockChain(1)


def test_basic_blockchain():
    """Test the basic blockchain"""

    # BlockChain without values
    blockchain = BlockChain()

    assert blockchain.last_block is not None
    assert blockchain.candidate_block is None
    assert blockchain.num_blocks == 1
    assert blockchain.is_valid

    # Manual definition of the genesis block
    block = Block.genesis_block(timestamp=datetime(2000, 1, 1), difficulty=4)
    blockchain = BlockChain(block)

    assert blockchain.last_block is None
    assert blockchain.candidate_block == block
    assert blockchain.num_blocks == 0
    assert blockchain.is_valid is False

    # it is not possible to add a new candidate
    assert blockchain.add_candidate(None) is False

    # Mining the candidate block
    assert blockchain.mining_candidate()

    # The blockchain is now valid
    assert blockchain.last_block == block
    assert blockchain.candidate_block is None
    assert blockchain.num_blocks == 1
    assert blockchain.is_valid


def test_block_repr():
    """Test the report function"""

    block = Block.genesis_block(timestamp=datetime(2000, 1, 1), difficulty=4, mining=True)
    blockchain = BlockChain(block)

    assert repr(blockchain) == \
           "Block: 0 (2000-01-01 00:00:00) - Hash: 015921ac58652b4e01d109cbb3ad10b55836e700a93e761036343ce8a82023ae\n"

    for minute in range(1, 6):
        blockchain.add_candidate(None, timestamp=datetime(2000, 1, 1, 0, minute, 0))
        blockchain.mining_candidate()

    assert repr(blockchain) == \
           "Block: 5 (2000-01-01 00:05:00) - Hash: 0332726221951b73e5fb945914341aa1e92014151680375cdf8c632256dc9a54\n" + \
           "Block: 4 (2000-01-01 00:04:00) - Hash: 0bf9e27631d08c326b15f7b459b47f91d9202c07ede76ce8503d636e09070402\n" + \
           "Block: 3 (2000-01-01 00:03:00) - Hash: 07ded3c477dc38fe3d0bc434b2924430f81231a0d7878f906e2a655c1f17d444\n" + \
           "Block: 2 (2000-01-01 00:02:00) - Hash: 0f8ed5b1cc4dca95c0c04b5b64a1ac409d636dbfd294282092f579d3872b1c15\n" + \
           "Block: 1 (2000-01-01 00:01:00) - Hash: 037eeba6b1779e5edd02e4a2b4909260193adaab7ef8abaf04ddc8ab2fc39c95\n" + \
           "\nand 1 block hidden"


def test_add_candidates():
    """Validate to include a new candidate"""

    block = Block.genesis_block(timestamp=datetime(2000, 1, 1), difficulty=4, mining=True)
    blockchain = BlockChain(block)

    assert blockchain.last_block == block
    assert blockchain.candidate_block is None
    assert blockchain.num_blocks == 1
    assert blockchain.is_valid

    # Add a new candidate
    assert blockchain.add_candidate(None, timestamp=datetime(2000, 1, 2))

    assert blockchain.last_block == block
    assert blockchain.candidate_block is not None
    assert blockchain.num_blocks == 1
    assert blockchain.is_valid

    # Fail in the mining process
    assert blockchain.mining_candidate(maximum_iter=0) is False

    # Mining the candidate block
    assert blockchain.mining_candidate()

    # The blockchain is now valid
    assert blockchain.last_block != block
    assert blockchain.candidate_block is None
    assert blockchain.num_blocks == 2
    assert blockchain.is_valid


def test_validate_blockchain():
    """Test BlockChain validation"""

    block = Block.genesis_block(timestamp=datetime(2000, 1, 1), difficulty=4, mining=True)
    blockchain = BlockChain(block)

    # Add a new candidate
    assert blockchain.add_candidate(None, timestamp=datetime(2000, 1, 2))
    assert blockchain.candidate_proof(4)

    assert blockchain.is_valid

    # Alter the index
    blockchain.chain[1].index = 2

    assert blockchain.chain[1].is_valid is False
    assert blockchain.is_valid is False

    # Mining new id
    blockchain.chain[1].mining()

    assert blockchain.chain[1].is_valid
    assert blockchain.is_valid is False

    # Change the block
    blockchain.chain[1] = block

    assert blockchain.is_valid is False


def test_add_candidates_prof():
    """Test to update the proof to a candidate"""

    block = Block.genesis_block(timestamp=datetime(2000, 1, 1), difficulty=4, mining=True)
    blockchain = BlockChain(block)

    # Add a new candidate
    assert blockchain.add_candidate(None, timestamp=datetime(2000, 1, 2))

    # Add proof to candidate
    assert blockchain.candidate_proof(3) is False
    assert blockchain.candidate_proof(4)

    # Add an empty candidate
    assert blockchain.add_candidate(None)

    # Add an invalid candidate (same date)
    assert blockchain.add_candidate(None, timestamp=datetime(2000, 1, 1)) is False

    assert blockchain.candidate_proof(3) is False
    assert blockchain.candidate_proof(4) is False


def test_mining_candidate():
    """Test mining candidate """

    block = Block.genesis_block(timestamp=datetime(2000, 1, 1), difficulty=4, mining=True)
    blockchain = BlockChain(block)

    # Add a new candidate
    assert blockchain.add_candidate(None, timestamp=datetime(2000, 1, 2))
    assert blockchain.mining_candidate()

    # Add an empty candidate
    assert blockchain.add_candidate(None)
    assert blockchain.mining_candidate()

    # Add an invalid candidate (same date)
    assert blockchain.add_candidate(None, timestamp=datetime(2000, 1, 1)) is False
    assert blockchain.mining_candidate() is False


def test_replace_chain():
    """Test replace a chain"""

    # Generate the genesis block
    block = Block.genesis_block(timestamp=datetime(2000, 1, 1), difficulty=4, mining=True)

    # Generate a old chain
    old_chain = BlockChain(block)

    # Generate longer chain
    blockchain = BlockChain(block)

    # Cannot be replace the chain
    assert old_chain.replace_chain(blockchain) is False

    # Add new block
    assert blockchain.add_candidate(None, timestamp=datetime(2000, 1, 2))
    assert blockchain.candidate_proof(4)

    # Replace the chain
    assert old_chain.replace_chain(blockchain)

    # Check the chain values
    assert old_chain.num_blocks == 2
    assert old_chain.candidate_block is None


def test_minimum_interval():
    """Test minimum interval period"""

    block = Block.genesis_block(timestamp=datetime(2000, 1, 1, 0, 0, 0), difficulty=4, mining=True)
    blockchain = BlockChain(block)

    # A block in a minute
    assert blockchain.add_candidate(None, timestamp=datetime(2000, 1, 1, 0, 1, 0))
    assert blockchain.mining_candidate()

    # A block in 30 seconds is not valid
    assert blockchain.add_candidate(None, timestamp=datetime(2000, 1, 1, 0, 1, 30)) is False


def test_update_difficulty():
    """Test increase and decrease difficulty values"""

    block = Block.genesis_block(timestamp=datetime(2000, 1, 1, 0, 0, 0), difficulty=4, mining=True)
    blockchain = BlockChain(block)

    # Change the interval for tests
    blockchain.difficulty_interval = 5

    # Blocks generates in a minute: the difficulty must increase
    for minute in range(1, 6):
        blockchain.add_candidate(None, timestamp=datetime(2000, 1, 1, 0, minute, 0))
        blockchain.mining_candidate()

    assert blockchain.chain[4].difficulty == 4
    assert blockchain.chain[5].difficulty == 5

    # Blocks generates in a eleven minutes: the difficulty must decrease
    for minute in range(17, 60, 11):
        blockchain.add_candidate(None, timestamp=datetime(2000, 1, 1, 0, minute, 0))
        blockchain.mining_candidate()

    blockchain.add_candidate(None, timestamp=datetime(2000, 1, 1, 1, 1, 0))
    blockchain.mining_candidate()

    assert blockchain.chain[9].difficulty == 5
    assert blockchain.chain[10].difficulty == 4


def test_change_block_contains():
    """Test different attacks to the blockchain"""

    data = ["Avocado", "Apple", "Cherry", "Orange", "Strawberry"]

    block = Block.genesis_block(data[0], timestamp=datetime(2000, 1, 1), difficulty=4, mining=True)
    blockchain = BlockChain(block)

    for minute in range(1, len(data)):
        assert blockchain.add_candidate(data[minute], timestamp=datetime(2000, 1, 1, 0, minute, 0))
        assert blockchain.mining_candidate()

    assert blockchain.is_valid

    # Alter the blockchain data
    blockchain.chain[2].data = 'Khaki'

    assert blockchain.is_valid is False
