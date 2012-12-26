# coding=utf-8

from functools import reduce
from unittest import TestCase

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util import Counter

from simplecrypt import encrypt, decrypt, _expand_keys, DecryptionException, \
    _random_bytes, HEADER, HALF_BLOCK, SALT_LEN


class TestEncryption(TestCase):

    def test_bytes_plaintext(self):
        ptext = decrypt('password', encrypt('password', b'message'))
        assert ptext == b'message', ptext

    def test_unicode_ciphertext(self):
        try:
            decrypt('password', 'some string')
            assert False, 'expected error'
        except DecryptionException as e:
            assert 'bytes' in str(e), e

    def test_bytes_password(self):
        ptext = decrypt(b'password', encrypt(b'password', b'message'))
        assert ptext == b'message', ptext
        ptext = decrypt('password', encrypt(b'password', b'message'))
        assert ptext == b'message', ptext
        ptext = decrypt(b'password', encrypt('password', b'message'))
        assert ptext == b'message', ptext

    def test_unicode_plaintext(self):
        ptext = decrypt('password', encrypt('password', 'message'))
        assert ptext.decode('utf8') == 'message', ptext
        ptext = decrypt('password', encrypt('password', 'message'.encode('utf8')))
        assert ptext == 'message'.encode('utf8'), ptext
        ptext = decrypt('password', encrypt('password', '¥£€$¢₡₢₣₤₥₦₧₨₩₪₫₭₮₯₹'))
        assert ptext.decode('utf8') == '¥£€$¢₡₢₣₤₥₦₧₨₩₪₫₭₮₯₹', ptext
        ptext = decrypt('password', encrypt('password', '¥£€$¢₡₢₣₤₥₦₧₨₩₪₫₭₮₯₹'.encode('utf8')))
        assert ptext == '¥£€$¢₡₢₣₤₥₦₧₨₩₪₫₭₮₯₹'.encode('utf8'), ptext

    def test_pbkdf(self):
        key = PBKDF2(b'password', b'salt')
        assert key == b'n\x88\xbe\x8b\xad~\xae\x9d\x9e\x10\xaa\x06\x12$\x03O', key

    def test_expand(self):
        key1, key2 = _expand_keys('password', b'salt')
        assert key1 != key2
        assert key1 == b'^\xc0+\x91\xa4\xb5\x9coY\xdd_\xbeL\xa6I\xec\xe4\xfa\x85h\xcd\xb8\xba6\xcfABn\x88\x05R+', key1
        assert len(key1) * 8 == 256, len(key1)
        assert key2 == b'\xa4\xe2\xae\xac\x19\xa4\x82\x15\x01\xcf`\x91&\xab\x01\xdf%f\x10\x83\xbff\xf9^R\x17\xfe\xe3\x19\x85\x04\xb1', key2
        assert len(key2) * 8 == 256, len(key2)

    def test_modification(self):
        ctext = bytearray(encrypt('password', 'message'))
        ctext[10] = ctext[10] ^ 85
        try:
            decrypt('password', ctext)
            assert False, 'expected error'
        except DecryptionException as e:
            assert 'modified' in str(e), e

    def test_bad_password(self):
        ctext = bytearray(encrypt('password', 'message'))
        try:
            decrypt('badpassword', ctext)
            assert False, 'expected error'
        except DecryptionException as e:
            assert 'Bad password' in str(e), e

    def test_empty_password(self):
        try:
            encrypt('', 'message')
            assert False, 'expected error'
        except ValueError as e:
            assert 'password' in str(e), e

    def test_distinct(self):
        enc1 = encrypt('password', 'message')
        enc2 = encrypt('password', 'message')
        assert enc1 != enc2

    def test_length(self):
        ctext = encrypt('password', '')
        assert not decrypt('password', ctext)
        try:
            decrypt('password', bytes(bytearray(ctext)[1:]))
            assert False, 'expected error'
        except DecryptionException as e:
            assert 'Missing' in str(e), e

    def test_prefix(self):
        ctext = bytearray(encrypt('password', 'message'))
        assert ctext[:len(HEADER)] == HEADER
        for i in range(len(HEADER)):
            ctext2 = bytearray(ctext)
            ctext2[i] = 1
            try:
                decrypt('password', ctext2)
                assert False, 'expected error'
            except DecryptionException as e:
                assert 'format' in str(e), e
        ctext2 = bytearray(ctext)
        ctext2[len(HEADER)] = 1
        try:
            decrypt('password', ctext2)
            assert False, 'expected error'
        except DecryptionException as e:
            assert 'format' not in str(e), e


class TestCounter(TestCase):

    def test_wraparound(self):
        # https://bugs.launchpad.net/pycrypto/+bug/1093446
        ctr = Counter.new(8, initial_value=255, allow_wraparound=False)
        try:
            ctr()
            ctr()
            assert False, 'expected error'
        except Exception as e:
            assert 'wrapped' in str(e), e
        ctr = Counter.new(8, initial_value=255, allow_wraparound=True)
        ctr()
        ctr()
        ctr = Counter.new(8, initial_value=255)
        try:
            ctr()
            ctr()
            assert False, 'expected error'
        except Exception as e:
            assert 'wrapped' in str(e), e

    def test_prefix(self):
        salt = _random_bytes(SALT_LEN//8)
        ctr = Counter.new(HALF_BLOCK, prefix=salt[:HALF_BLOCK//8])
        count = ctr()
        assert len(count) == AES.block_size, count


class TestRandBytes(TestCase):

    def test_bits(self):
        b = _random_bytes(100) # test will fail ~ 1 in 2^100/8 times
        assert len(b) == 100
        assert 0 == reduce(lambda x, y: x & y, bytearray(b)), b
        assert 255 == reduce(lambda x, y: x | y, bytearray(b)), b

    def test_all_values(self):
        b = _random_bytes(255*10)
        assert reduce(lambda a, b: a and b, (n in b for n in range(256)), True)
        b = _random_bytes(255)
        assert not reduce(lambda a, b: a and b, (n in b for n in range(256)), True)
