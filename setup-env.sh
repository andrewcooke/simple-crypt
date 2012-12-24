#!/bin/bash

virtualenv --python=python3.2 env
source env/bin/activate
easy_install pycrypto

