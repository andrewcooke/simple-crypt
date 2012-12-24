
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util import Counter


COUNT = 1000
AES_KEY_LEN = 256//8  # pycrypto uses bytes, not bits
HMAC_HASH = SHA256
COUNTER_SIZE = 128


def encrypt(salt, password, data):
    '''
    Encrypt some data.

    @param salt: A string, at least 8 characters long, that must be identical
     to the value passed to `decrypt`, but which should otherwise vary as
     much as possible between uses.  For example, if the encryption is
     specific to a particular user then you could use the user's name.  The
     idea is not that this value is secret, but that it adds additional
     variation to the data.  At the very least, you could use the name of
     your application here.

    @param password: A string, the secret value used as the basis for a key.
     This should be as long as varied as possible.  Try to avoid common words.

    @param data: The data to be encrypted, typically as bytes.  You can pass
     in a simple string, which will be encoded as utf8.

    @return: The encrypted data, as bytes.
    '''
    key = _expand_key(salt, password)
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(COUNTER_SIZE))
    ctext = cipher.encrypt(data)
    hmac = HMAC.new(key, ctext, HMAC_HASH).digest()
    return ctext + hmac


def decrypt(salt, password, ctext):
    '''
    Decrypt some data.

    @param salt: A string, at least 8 characters long, that must be identical
     to the value passed to `encrypt`, but which should otherwise vary as
     much as possible between uses.  For example, if the encryption is
     specific to a particular user then you could use the user's name.  The
     idea is not that this value is secret, but that it adds additional
     variation to the data.  At the very least, you could use the name of
     your application here.

    @param password: A string, the secret value used as the basis for a key.
     This should be as long as varied as possible.  Try to avoid common words.

    @param data: The data to be decrypted, typically as bytes.  You can pass
     in a simple string, which will be encoded as utf8.

    @return: The decrypted data, as bytes.
    '''
    key = _expand_key(salt, password)
    hmac2 = HMAC.new(key, ctext[:-HMAC_HASH.digest_size], HMAC_HASH).digest()
    hmac = ctext[-HMAC_HASH.digest_size:]
    if hmac != hmac2: raise Exception("data were modified")
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(COUNTER_SIZE))
    ctext = ctext[:-HMAC_HASH.digest_size]
    return cipher.decrypt(ctext)


def _expand_key(salt, password):
    return PBKDF2(password.encode('utf8'), salt.encode('utf8'), dkLen=AES_KEY_LEN, count=COUNT)
