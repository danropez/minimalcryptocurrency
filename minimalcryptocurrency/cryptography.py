"""Cryptography functions"""

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


from ecdsa import SigningKey, VerifyingKey, BadSignatureError


def generate_public_key(key):
    """Generate the public key

    Generate the public key for a private key in hex format.

    Args:
        key (String): a private key

    Return:
        (String): the public key for the private key
    """

    sk = SigningKey.from_string(bytes.fromhex(key))

    return sk.get_verifying_key().to_string().hex()


def is_signature_valid(message, signature, public_key):
    """Validate if a message has a valid signature

    Args:
        message (String): the message which has been signed
        signature (String): the signature of the message
        public_key (String): the public key

    Return:
        (Logical): True if the message has been signed by the public key
    """

    try:
        vk = VerifyingKey.from_string(bytes.fromhex(public_key))
        return vk.verify(bytes.fromhex(signature), message.encode('utf-8'))
    except AssertionError:
        # The key is not valid
        return False
    except BadSignatureError:
        # The signature is not valid
        return False

    return False


def signature(message, key):
    """Calculate the signature of a message

    Args:
        message (String): the message which has been signed
        key (String): the private key

    Return:
        (String): the signature of the message
    """

    sk = SigningKey.from_string(bytes.fromhex(key))

    return sk.sign(message.encode('utf-8')).hex()
