#!/bin/bash

rm -fr env-3.3
virtualenv-3.4 --python=python3.3 env-3.3
source env-3.3/bin/activate
#easy_install pycrypto
#easy_install nose
pip install ~/Downloads/pycrypto-2.6.1.tar.gz
pip install ~/Downloads/nose-1.3.7.tar.gz

