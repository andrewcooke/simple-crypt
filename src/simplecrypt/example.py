
from binascii import hexlify
from getpass import getpass
from sys import stdin

from simplecrypt import encrypt, decrypt

# read the password from the user (without displaying it)
password = getpass("password: ")

# read the (single line) plaintext we will encrypt
print("message: ")
message = stdin.readline()

# encrypt the plaintext.  we explicitly convert to bytes first (optional)
ciphertext = encrypt(password, message.encode('utf8'))

# the ciphertext plaintext is bytes, so we display it as a hex string
print("ciphertext: %s" % hexlify(ciphertext))

# now decrypt the plaintext (using the same salt and password)
plaintext = decrypt(password, ciphertext)

# the decrypted plaintext is bytes, but we can convert it back to a string
print("plaintext: %s" % plaintext)
print("plaintext as string: %s" % plaintext.decode('utf8'))
