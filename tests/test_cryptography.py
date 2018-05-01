"""Tests for the cryptography functions"""

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


from minimalcryptocurrency import generate_public_key
from minimalcryptocurrency import is_signature_valid
from minimalcryptocurrency import signature


def test_generate_public_key():
    """Test conversion of private key to public key"""

    key = generate_public_key('d1aa1463063a412e92fbc11dd1c65bff72ae862ea3f888a6')

    assert key == '388d9128602032c62e3fda1e1d595bc2b03a4482fc896cee33c439e673a0094213e5120b88f1725bca72bbe07520e643'


def test_is_signature_valid():
    """Test the functions which validates signatures"""

    assert is_signature_valid('First',
                              '4f3ad4cc53704930e2e5963e529690c46711dbb2e2bdcdf7ca86bfd679532fdd3b920e597ad0556d4e781aa353caa124',
                              '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c')
    assert is_signature_valid('Second',
                              'd2d74e5f661d84ee5ecee5087aeeefe364686e7cb3561ebf5fa33f92930d2add2ff5f6c468a94950e63c38e92900ee27',
                              '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c')

    assert is_signature_valid('First',
                              'd2d74e5f661d84ee5ecee5087aeeefe364686e7cb3561ebf5fa33f92930d2add2ff5f6c468a94950e63c38e92900ee27',
                              '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c') is False


def test_signature():
    """Test the generation of signatures"""

    assert is_signature_valid('First',
                              signature('First', 'aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518'),
                              '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c')
    assert is_signature_valid('Second',
                              signature('Second', 'aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518'),
                              '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c')

    assert is_signature_valid('Other',
                              signature('Second', 'aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518'),
                              '55d83bb921c148822bfe7057604bf3bb6d499976ea1054943f91c9caf28f2717bfcdf5e5b8c1fc0d18d510691765506c') is False

    assert is_signature_valid('Other',
                              signature('Other', 'aedc3975fa118bec4a1d203cd2b996c4ceb5aa398b7f7518'),
                              'd2d74e5f661d84ee5ecee5087aeeefe364686e7cb3561ebf5fa33f92930d2add2ff5f6c468a94950e63c38e92900ee27') is False
