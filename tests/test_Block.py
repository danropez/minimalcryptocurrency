"""Tests for the Block object"""

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


def test_creation_block():
    """Test errors during the construcion of an object"""

    with pytest.raises(Exception):
        Block()


def test_block_basic():
    """Test the definition of a basic Block"""

    block = Block(0, 'block data')

    assert block.index == 0
    assert block.previous_hash is None
    assert block.difficulty == 0
    assert block.data == 'block data'
    assert block.proof == 0

    block = Block(1, 'block data', timestamp=0)

    assert block.index == 1
    assert block.previous_hash is None
    assert block.difficulty == 0
    assert block.data == 'block data'
    assert block.proof == 0
    assert block.timestamp == 0
    assert block.hash == 'bc9ef25d3e98e4fd29add80d59b5ffc315176b8de85167569be118c9f3f42c2b'

    # Next block evaluation
    block = Block(block, 'Second block', timestamp=1)

    assert block.index == 2
    assert block.previous_hash == 'bc9ef25d3e98e4fd29add80d59b5ffc315176b8de85167569be118c9f3f42c2b'
    assert block.difficulty == 0
    assert block.data == 'Second block'
    assert block.proof == 0
    assert block.timestamp == 1
    assert block.hash == '5641942dc909b7a89f79a0d8bc022aca797cc66001194d82711cc508e90e997b'

    # Validate hash calculation
    assert Block.calculate_hash(block) == block.hash


def test_block_repr():
    """Test the report function"""

    assert repr(Block(0, ' data', timestamp=0)) == \
           'Block: 0 (0)\n Hash: d8345cd456a98ac9533f1c9f662685318413d76333741100ecdf34b112488e5e\n Previous: None'


def test_block_comparisons():
    """Test the comparison of different blocks"""

    block_0 = Block(0, 'block data', timestamp=0)
    block_1 = Block(0, 'block data', timestamp=0)
    block_2 = Block(1, 'block data', timestamp=0)

    assert block_0 == block_0
    assert block_0 == block_1
    assert block_0 != block_2


def test_block_difficulty():
    """Test proof-of-work validation"""

    block = Block(0, 'Test Data', timestamp=0)

    assert block.hash_satisfies_difficulty

    block.difficulty = 4

    assert block.hash_satisfies_difficulty is False

    block.proof = 49

    assert block.proof == 49
    assert block.hash_satisfies_difficulty

    block.proof = 5

    assert block.proof == 5
    assert block.hash_satisfies_difficulty is False


def test_block_valid():
    """Test validation of a block"""

    block = Block(0, 'Test Data', timestamp=0)

    assert block.hash_satisfies_difficulty
    assert block.is_valid

    block.difficulty = 4

    assert block.hash_satisfies_difficulty is False
    assert block.is_valid is False

    block.proof = 49

    assert block.proof == 49
    assert block.hash_satisfies_difficulty
    assert block.is_valid

    # Introduce a fake hash
    block.hash = '0f59bbd5a22a6484cc206b7ee9d4bc1744bed9c5649ff332f88a0eec461f58c8'

    assert block.hash == '0f59bbd5a22a6484cc206b7ee9d4bc1744bed9c5649ff332f88a0eec461f58c8'
    assert block.hash_satisfies_difficulty
    assert block.is_valid is False


def test_mining():
    """Test the mining process in the Block"""

    block = Block(0, 'Test data', timestamp=0)

    block.difficulty = 8

    assert block.hash_satisfies_difficulty is False
    assert block.is_valid is False

    # Calculate a valid proof
    assert block.mining()

    assert block.hash_satisfies_difficulty
    assert block.is_valid

    # Set a value which cannot get a valid result
    assert block.mining(init=0, maximum_iter=100) is False

    assert block.hash_satisfies_difficulty is False
    assert block.is_valid is False


def test_genesis_block():
    """Validate the genesis block test"""

    block = Block.genesis_block(timestamp=datetime(2000, 1, 1), difficulty=6, mining=True)

    assert block.index == 0
    assert block.previous_hash == '5e9fe54187feed1f12324ffa7bd9dc3d662706e1fd66a97eafbbefa912262aa2'
    assert block.difficulty == 6
    assert block.hash == '01392e12860c25f46adad36d001d9c9aeafc280cf8be290021e61c2ec2cb54de'
    assert block.timestamp == datetime(2000, 1, 1)
    assert block.data is None
    assert block.proof == 46
