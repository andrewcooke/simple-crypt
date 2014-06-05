#!/bin/bash

virtualenv-3.3 --python=python3.0 env-3.0
source env-3.0/bin/activate
easy_install pycrypto
easy_install nose
