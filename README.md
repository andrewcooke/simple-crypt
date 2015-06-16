# simple-crypt

Simple, secure encryption and decryption for Python 2.7 and 3.

Now on [pypi](http://pypi.python.org/pypi/simple-crypt):
```pip install simple-crypt```
(note that the pypi name includes a hyphen).

This provides two functions, which encrypt and decrypt data, delegating all
the hard work to the [pycrypto](https://www.dlitz.net/software/pycrypto)
library (which must also be installed).

## Examples

### The API

The two calls:

```python
from simplecrypt import encrypt, decrypt

ciphertext = encrypt(password, 'my secret message')
plaintext = decrypt(password, ciphertext)
```

### Interactive Use

A simple Python 3 program:

```python
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
```

Which, when run, produces something like the following (the actual encrypted
message will be different each time, as a random salt is used for each
message):

```
password: ******

message:
hello world
ciphertext: b'73630001b1c39575390d5720f2a80e7a06fbddbf2c844d6b8eaf845d4a9e140d46a54c6729e74b0ddeb1cb82dee81691123faf8f41900c5a6c5b755ed8ae195ff2410290bcb8dc2ee3a2126c594b711d'
plaintext: b'hello world\n'
plaintext as string: hello world
```

Also, it's perhaps worth noting that the overhead (the extra length of the
encrypted data, compared to the message) is constant.  It looks a lot here,
because the message is very small, but for most practical uses should not be
an issue.

### Using Files

When the following program is run, if the file "encrypted.txt" does not
exist, then it is created with the contents "10 green bottles".

If the file does exist, it is read, and the number of green bottles is
reduced.  If there are no green bottles left, then the file is
deleted, otherwise it is written with the new number.


```python
from simplecrypt import encrypt, decrypt
from os.path import exists
from os import unlink

PASSWORD = "secret"
FILENAME = "encrypted.txt"

def main():
    # read or create the file
    if exists(FILENAME):
        print("reading...")
        data = read_encrypted(PASSWORD, FILENAME)
        print("read %s from %s" % (data, FILENAME))
        n_bottles = int(data.split(" ")[0]) - 1
    else:
        n_bottles = 10
    # write the file
    if n_bottles > 0:
        data = "%d green bottles" % n_bottles
        print("writing...")
        write_encrypted(PASSWORD, FILENAME, data)
        print("wrote %s to %s" % (data, FILENAME))
    else:
        unlink(FILENAME)
        print("deleted %s" % FILENAME)

def read_encrypted(password, filename, string=True):
    with open(filename, 'rb') as input:
        ciphertext = input.read()
        plaintext = decrypt(password, ciphertext)
        if string:
            return plaintext.decode('utf8')
        else:
            return plaintext

def write_encrypted(password, filename, plaintext):
    with open(filename, 'wb') as output:
        ciphertext = encrypt(password, plaintext)
        output.write(ciphertext)

if __name__ == '__main__':
    main()
```

This program is included in
[src/simplecrypt/example-file.py](src/simplecrypt/example-file.py) and
we can run it as follows:

```
> python3 src/simplecrypt/example-file.py
writing...
wrote 10 green bottles to encrypted.txt
> python3 src/simplecrypt/example-file.py
reading...
read 10 green bottles from encrypted.txt
writing...
wrote 9 green bottles to encrypted.txt
> 
...
> python3 src/simplecrypt/example-file.py
reading...
read 1 green bottles from encrypted.txt
deleted encrypted.txt
>
```

## Alternatives

This code is intended to be "easy to use" and "hard to use wrong".  An
alternative for more experienced users (who might, for example, want
to use more rounds in the PBKDF, or an explicit key) is
[python-aead](https://github.com/Ayrx/python-aead).

As far as I can tell, python-aead uses very similar algorithms to
those found here.

## Algorithms

The algorithms used follow the recommendations at
http://www.daemonology.net/blog/2009-06-11-cryptographic-right-answers.html 
and http://www.daemonology.net/blog/2009-06-24-encrypt-then-mac.html,
as far as I can tell:

* The password is expanded to two 256 bit keys using PBKDF2 with a 256 bit
  random salt (increased from 128 bits in release 3.0.0), SHA256, and
  100,000 iterations (increased from 10,000 in release 4.0.0).

* AES256 CTR mode is used to encrypt the data with one key.  The first 64 bits
  of the salt are used as a message nonce (of half the block size); the
  incremental part of the counter uses the remaining 64 bits (see section B.2
  of http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf).

* An encrypted messages starts with a 4 byte header ("sc" in ASCII followed
  by either two zero bytes (pre-3.0), or a zero and a one).

* An SHA256 HMAC (of header, salt, and encrypted message) is calculated using
  the other key.

* The final message consists of the header, salt, encrypted data, and HMAC,
  concatenated in that order.

* On decryption, the header is checked and the HMAC validated before
  decryption.

The [entire implementation is here](https://github.com/andrewcooke/simple-crypt/blob/master/src/simplecrypt/__init__.py).

Discussion and criticism of the design can be found on
[HN](http://news.ycombinator.com/item?id=4962983)
([also](https://news.ycombinator.com/item?id=6194102)),
[codereview.stackexchange](http://codereview.stackexchange.com/questions/19910/simple-crypto-library-in-python-correct-and-secure)
and
[crypto.stackexchange](http://crypto.stackexchange.com/questions/5843/future-proof-versioning-and-validation).
Grateful thanks to all commentators (particularly marshray); mistakes remain
mine.

Please note that the general design, based on the [cryptographic right
answers](http://www.daemonology.net/blog/2009-06-11-cryptographic-right-answers.html),
is intended to give 128 bits of security - any attack would require around
2^128 guesses.  This comes from birthday collisions on the 256 bit HMAC and
random numbers (since release 3.0).  AES256 is used because it provides
additional security if, for example, some key bits are revealed through timing
attacks (see link above or chapter 7 of Practical Cryptography).

## Latest News

Release 4.1 obscures the output of the random number generator.  This should
not be necessary, but guards against a possible attack if the random number
generator is compromised in some way.  Functionality and interoperability are
otherwise unchanged.

Release 4.0 increases the number of iterations used in the PBKDF (this
will make encryption and decryption noticeably slower) and adds a
reference to [python-aead](https://github.com/Ayrx/python-aead).

Release 3.0 [increases the size of the salt used from 128 to 256
bits](http://acooke.org/cute/ChangingSa0.html).

The header changes with each major version release (after 2.0), so
data encrypted by previous releases can be detected and decrypted
correctly.  However, data encrypted by later major releases (after
2.0) cannot be decrypted by earlier releases (instead, an error with a
helpful message is generated).

Release 2.0 was fully compatible with 1.0 on Python 3 (same API and
identical results).  However, thanks to
[d10n](https://github.com/d10n) it also supported Python 2.7 (tested
with Python 2.7.5, 3.0.1 and 3.3.2).

I (Andrew Cooke) am not sure Python 2.7 support is such a good idea.  You should
really use something like [keyczar](http://www.keyczar.org/).  But there seems
to be a demand for this, so better the devil you know...

## Warnings

1. The whole idea of encrypting with a password is not so smart these days.
   If you think you need to do this, try reading about Google's
   [keyczar](http://www.keyczar.org/) which instead uses a keystore
   (unfortunately, at the time of writing, keyczar does not support Python 3,
   as far as I can tell, but that should change soon).

2. When you call these routines the password is stored in memory as a Python
   string.  This means that malicious code running on the same machine might
   be able to read the password (or even that the password could be written to
   swap space on disk).  One way to reduce the risk is to have the crypto part
   of your code run as a separate process that exists for a limited time.

3. All encrypted messages start with a 4 byte header (ASCII "sc", followed
   by the version number).  So an adversary is able to recognize that the 
   data are encrypted (and not simply random).  You can avoid this by discarding
   the first 4 bytes of the encrypted data, but you must of course replace them
   before decrypting, and the code will not inter-operate between versions.

4. I have considered extending the code to handle inputs larger than can
   be held in memory.  While this is possible, the HMAC is not validated until
   decrypted data are returned.  Which is asking for trouble - people are
   going to use the data as they are decrypted - and shows that the current
   design is inappropriate for such use.  Someone needs to design a better
   solution (eg. with HMAC checks for each "block" - but even that allows
   data to be silently truncated at the end of a block).

(c) 2012-2015 Andrew Cooke, andrew@acooke.org; 2013
[d10n](https://github.com/d10n), david@bitinvert.com.  Released into the
public domain for any use, but with absolutely no warranty.
