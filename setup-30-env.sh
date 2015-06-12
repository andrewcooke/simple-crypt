#!/bin/bash

# remember you may need 'export SVNVERSION="XX"' when installing Python 3.0

rm -fr env-3.0
virtualenv-3.4 --python=python3.0 env-3.0
source env-3.0/bin/activate
#easy_install pycrypto
#easy_install nose
pip install ~/Downloads/pycrypto-2.6.1.tar.gz
pip install ~/Downloads/nose-1.3.7.tar.gz
