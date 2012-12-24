
from functools import reduce

from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random.random import getrandbits
from Crypto.Util import Counter


EXPANSION_COUNT = 1000
AES_KEY_LEN = 256
HMAC_HASH = SHA256


def encrypt(salt, password, data):
    '''
    Encrypt some data.

    @param salt: A string, at least 8 characters long, that must be identical
     to the value passed to `decrypt`, but which should otherwise vary as
     much as possible between uses.  For example, if the encryption is
     specific to a particular user then you could use the user's name.  The
     idea is not that this value is secret, but that it adds additional
     variation to the key.  At the very least, you could use the name of
     your application here.

    @param password: A string, the secret value used as the basis for a key.
     This should be as long as varied as possible.  Try to avoid common words.

    @param data: The data to be encrypted, typically as bytes.  You can pass
     in a simple string, which will be encoded as utf8.

    @return: The encrypted data, as bytes.
    '''
    key = _expand_key(salt, password)
    offset = getrandbits(AES.block_size*8)
    counter = Counter.new(AES.block_size*8, initial_value=offset, allow_wraparound=True)
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)
    encrypted = cipher.encrypt(data)
    prefix = bytes(_offset_to_bytes(offset))
    hmac = HMAC.new(key, prefix + encrypted, HMAC_HASH).digest()
    return prefix + encrypted + hmac


def decrypt(salt, password, data):
    '''
    Decrypt some data.

    @param salt: A string, at least 8 characters long, that must be identical
     to the value passed to `encrypt`, but which should otherwise vary as
     much as possible between uses.  For example, if the encryption is
     specific to a particular user then you could use the user's name.  The
     idea is not that this value is secret, but that it adds additional
     variation to the key.  At the very least, you could use the name of
     your application here.

    @param password: A string, the secret value used as the basis for a key.
     This should be as long as varied as possible.  Try to avoid common words.

    @param data: The data to be decrypted, typically as bytes.  You can pass
     in a simple string, which will be encoded as utf8.

    @return: The decrypted data, as bytes.
    '''
    key = _expand_key(salt, password)
    hmac = data[-HMAC_HASH.digest_size:]
    hmac2 = HMAC.new(key, data[:-HMAC_HASH.digest_size], HMAC_HASH).digest()
    if hmac != hmac2: raise Exception("data were modified")
    offset = _bytes_to_offset(data[:AES.block_size])
    counter = Counter.new(AES.block_size*8, initial_value=offset, allow_wraparound=True)
    cipher = AES.new(key, AES.MODE_CTR, counter=counter)
    return cipher.decrypt(data[AES.block_size:-HMAC_HASH.digest_size])


def _expand_key(salt, password):
    return PBKDF2(password.encode('utf8'), salt.encode('utf8'), dkLen=AES_KEY_LEN//8, count=EXPANSION_COUNT)

def _offset_to_bytes(offset):
    for _ in range(AES.block_size):
        yield offset % 256
        offset //= 256

def _bytes_to_offset(bytes):
    return reduce(lambda x, y: x * 256 + y, reversed(bytearray(bytes)))
