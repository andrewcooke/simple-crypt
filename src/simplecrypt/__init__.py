
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util import Counter

COUNT=1000
AES_KEY_LEN=256//8 # bytes used in pycrypto
HMAC_HASH=SHA256

def encrypt(salt, password, ptext):
    key = _expand_key(salt, password)
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
    ctext = cipher.encrypt(ptext)
    hmac = HMAC.new(key, ctext, HMAC_HASH).digest()
    return ctext + hmac

def decrypt(salt, password, ctext):
    key = _expand_key(salt, password)
    hmac2 = HMAC.new(key, ctext[:-HMAC_HASH.digest_size], HMAC_HASH).digest()
    hmac = ctext[-HMAC_HASH.digest_size:]
    if hmac != hmac2: raise Exception("data were modified")
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
    ctext = ctext[:-HMAC_HASH.digest_size]
    return cipher.decrypt(ctext)

def _expand_key(salt, password):
    return PBKDF2(password.encode('utf8'), salt.encode('utf8'), dkLen=AES_KEY_LEN, count=COUNT)

