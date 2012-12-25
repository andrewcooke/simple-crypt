
from binascii import hexlify
from getpass import getpass
from sys import stdin

from simplecrypt import encrypt, decrypt

# read the password from the user (without displaying it)
password = getpass("password: ")

# read the (single line) message we will encrypt
print("message: ")
message = stdin.readline()

# encrypt the message.  we explicitly convert to bytes first (optional)
encrypted = encrypt(password, message.encode('utf8'))

# the encrypted message is bytes, so we display it as a hex string
print("encrypted message: %s" % hexlify(encrypted))

# now decrypt the message (using the same salt and password)
decrypted = decrypt(password, encrypted)

# the decrypted message is bytes, but we can convert it back to a string
print("decrypted message: %s" % decrypted)
print("decrypted string: %s" % decrypted.decode('utf8'))
