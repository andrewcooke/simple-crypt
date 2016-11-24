#!/bin/bash

rm large*
head -c 10M < /dev/urandom > large.1
PYTHONPATH=.. ./example-cmd.py -o large.2 -p secret large.1
PYTHONPATH=.. ./example-cmd.py -o large.3 -p secret large.2
ls -l --block-size=M large*
sha1sum large*
diff -s large.1 large.3
