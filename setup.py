
from distutils.core import setup

setup(
    name = 'simple-crypt',
    url = 'https://github.com/andrewcooke/simple-crypt',
    requires = 'pycrypto',
    packages = ['simplecrypt'],
    package_dir = {'': 'src'},
    version = '0.1.7',
    description = 'Simple encryption and decryption for Python 3',
    author = 'Andrew Cooke',
    author_email = 'andrew@acooke.org',
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: Public Domain',
                   'Programming Language :: Python :: 3',
                   'Topic :: Security',
                   'Topic :: Security :: Cryptography',
                   'Topic :: Software Development'],
    long_description = '''
What Does Simple Crypt Do?
--------------------------

Simple Crypt encrypts and decrypts data.  It has two functions, ``encrypt``
and ``decrypt``::

    from simplecrypt import encrypt, decrypt
    encrypted = encrypt('password', plaintext)
    plaintext = decrypt('password', encrypted)

That's it.  You can see the implementation on
`github <https://github.com/andrewcooke/simple-crypt/blob/master/src/simplecrypt/__init__.py>`_.

Why Should You Use Simple Crypt?
--------------------------------

* It uses standard, well-known algorithms, closely following the
  recommendations `here <http://www.daemonology.net/blog/2009-06-11-cryptographic-right-answers.html>`_.

* It uses routines from the established `pycrypto <https://www.dlitz.net/software/pycrypto>`_
  library (the cipher used is AES256).

* It includes a check (an HMAC with SHA256) to warn when encrypted data are
  modified.

* It tries to make things as secure as possible when poor quality passwords
  are used (PKBDF2 with SHA256, a 128 bit salt, and 10,000 rounds).  But that
  doesn't mean you should use a poor password!

* Using a library, rather than writing your own code, means that we have less
  solutions to the same problem.  That means more chance of finding bugs, which
  means more reliable, more secure code.

What Else Should I Know?
------------------------

* You must also install ``pycrypto``.

* The outputs from ``encrypt`` and ``decrypt`` are ``bytes``.  If you started
  with string input then you can convert the output from ``decrypt`` using
  ``.decode('utf8')``.

::

    mystring = decrypt('password', encrypted).decode('utf8')
    '''
)
