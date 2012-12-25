simple-crypt
============

Simple encryption and decryption for Python 3.

This provides two functions, which encrypt and decrypt data, delegating all
the hard work to the [pycrypto](https://www.dlitz.net/software/pycrypto)
library (which must also be installed).

Examples
--------

The two calls:

```python
encrypted = encrypt(password, 'my secret')
decrypted = decrypt(password, encrypted)
```

A simple program:

```python
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
```

Which, when run, produces something like the following (the actual encrypted
message will be different each time, as a random IV is used for each message):

```
password: ******

message:
hello world
encrypted message: b'7363000065c876f96113f1aea09438d66ad01ebc8049fab25d0ad7bd6f85b0f5b2574138e410b9e966ac54c8130483b6e89ebe69f87e1f519afc2f848bfecccf'
decrypted message: b'hello world\n'
decrypted string: hello world
```

Also, it's perhaps worth noting that the overhead (the extra length of the
encrypted data, compared to the message) is constant.  It looks a lot here,
because the message is very small, but for most practical uses should not be
an issue.

Algorithms
----------

The algorithms used follow the recommendations at
http://www.daemonology.net/blog/2009-06-11-cryptographic-right-answers.html,
as far as I can tell:

* The "password" is expanded to a 256 bit key, using PBKDF2 with a 128 bit
  random "salt".

* AES256 CTR mode is used to encrypt the data.  The first 64 bits of the
  salt are used as a nonce; the associated counter is 64 bits
  (see http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf).

* A SHA256 HMAC (of salt plus encrypted message) is calculated and
  appended.  This uses the same key as the AES cipher.

* On decryption, the HMAC is validated before decryption.

The [entire implementation is here](https://github.com/andrewcooke/simple-crypt/blob/master/src/simplecrypt/__init__.py).
