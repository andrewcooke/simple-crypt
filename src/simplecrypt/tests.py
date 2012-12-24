# coding=utf-8

from unittest import TestCase

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random.random import getrandbits
from Crypto.Util import Counter

from simplecrypt import encrypt, decrypt, _expand_key, _bytes_to_offset, _offset_to_bytes


class TestEncryption(TestCase):

    def test_bytes(self):
        ptext = decrypt('salt', 'password', encrypt('salt', 'password', b'message'))
        assert ptext == b'message', ptext

    def test_unicode(self):
        ptext = decrypt('salt', 'password', encrypt('salt', 'password', 'message'))
        assert ptext.decode('utf8') == 'message', ptext
        ptext = decrypt('salt', 'password', encrypt('salt', 'password', 'message'.encode('utf8')))
        assert ptext == 'message'.encode('utf8'), ptext
        ptext = decrypt('salt', 'password', encrypt('salt', 'password', '¥£€$¢₡₢₣₤₥₦₧₨₩₪₫₭₮₯₹'))
        assert ptext.decode('utf8') == '¥£€$¢₡₢₣₤₥₦₧₨₩₪₫₭₮₯₹', ptext
        ptext = decrypt('salt', 'password', encrypt('salt', 'password', '¥£€$¢₡₢₣₤₥₦₧₨₩₪₫₭₮₯₹'.encode('utf8')))
        assert ptext == '¥£€$¢₡₢₣₤₥₦₧₨₩₪₫₭₮₯₹'.encode('utf8'), ptext

    def test_pbkdf(self):
        key = PBKDF2(b'password', b'salt')
        assert key == b'n\x88\xbe\x8b\xad~\xae\x9d\x9e\x10\xaa\x06\x12$\x03O', key

    def test_expand(self):
        key = _expand_key('salt', 'password')
        assert key == b'n\x88\xbe\x8b\xad~\xae\x9d\x9e\x10\xaa\x06\x12$\x03O\xedH\xd0?\xcb\xad\x96\x8bV\x00g\x84S\x9dR\x14', key
        assert len(key) * 8 == 256, len(key)

    def test_modification(self):
        ctext = bytearray(encrypt('salt', 'password', 'message'))
        ctext[10] = ctext[10] ^ 85
        try:
            decrypt('salt', 'password', ctext)
            assert False, 'expected error'
        except Exception as e:
            assert 'modified' in str(e), e


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

    def test_offset(self):
        self.assert_offset(0)
        self.assert_offset(1)
        self.assert_offset(255)
        self.assert_offset(256)
        self.assert_offset(2**128-1)
        for _ in range(100):
            self.assert_offset(getrandbits(AES.block_size))

    def assert_offset(self, offset):
        result = _bytes_to_offset(_offset_to_bytes(offset))
        assert result == offset, (result, offset, bytes(_offset_to_bytes(offset)))
