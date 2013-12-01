#!/bin/bash

virtualenv-2.7 --python=python2.7 env-2.7
source env-2.7/bin/activate
easy_install pycrypto

