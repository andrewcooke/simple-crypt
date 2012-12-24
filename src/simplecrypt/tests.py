
from unittest import TestCase
from Crypto.Protocol.KDF import PBKDF2
from simplecrypt import encrypt, decrypt, _expand_key

class TestEncryption(TestCase):

    def test_known_result(self):
        ctext = encrypt('salt', 'password', 'message')
        assert ctext == b"F\xb5\x10\xd2\x10\x05\xfe\xcfl\x07~\xbf^\xbc\x8b\x0c\xecw\xe1\xe0#'\x11\xc9\xbf\x19\t\t?aF\xb5<\xede\x1e\xdb$\xfa", ctext

    def test_roundtrip(self):
        ptext = decrypt('salt', 'password', encrypt('salt', 'password', 'message'))
        assert ptext == 'message'.encode('utf8'), ptext

    def test_pbkdf(self):
        key = PBKDF2(b'password', b'salt')
        assert key == b'n\x88\xbe\x8b\xad~\xae\x9d\x9e\x10\xaa\x06\x12$\x03O', key

    def test_expand(self):
        key = _expand_key('salt', 'password')
        assert key == b'n\x88\xbe\x8b\xad~\xae\x9d\x9e\x10\xaa\x06\x12$\x03O\xedH\xd0?\xcb\xad\x96\x8bV\x00g\x84S\x9dR\x14', key
        assert len(key) * 8 == 256, len(key)
