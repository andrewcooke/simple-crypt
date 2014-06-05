#!/bin/bash

rm -fr env-3.3
virtualenv-3.3 --python=python3.3 env-3.3
source env-3.3/bin/activate
easy_install pycrypto
easy_install nose
