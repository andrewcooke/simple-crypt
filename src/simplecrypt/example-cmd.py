#!/usr/bin/env python

from simplecrypt import encrypt, decrypt, HEADER, HEADER_LEN

from sys import argv, stdin, stdout
from getpass import getpass

# an example command that either encrypts or decrypts data.

def print_usage():
    print("")
    print("encrypt or decrypt data")
    print("")
    print("usage:")
    print("")
    print(" %s [-h] [-p pwd] [-e|-d] [-o outfile] [infile]" % argv[0])
    print("")
    print("         -h: print this message and exit")
    print("     -p pwd: provide a password (or interactive prompt)")
    print("         -e: encrypt (or auto-detect)")
    print("         -d: decrypt (or auto-detect)")
    print(" -o outfile: output file (or stdout)")
    print("     infile: the file to encrypt (or stdin)")
    print("")
    exit(1)

def parse_args():
    password = None; infile = stdin; action = None
    try:
        outfile = stdout.buffer  # python 3 for bytes
    except AttributeError:
        outfile = stdout         # python 2
    args = list(argv[1:])
    while args:
        head = args.pop(0)
        if head == '-p':
            password = args.pop(0)
        elif head == '-e':
            action = encrypt
        elif head == '-d':
            action = decrypt
        elif head == '-o':
            outfile = open(args.pop(0), 'wb')
        elif not args and not head.startswith('-'):
            infile = open(head, 'rb')
        else:
            print_usage()
    return password, infile, outfile, action

def main():
    password, infile, outfile, action = parse_args()
    if password is None:
        password = getpass("password: ")
    indata = infile.read()
    if action is None:
        if indata[:HEADER_LEN] in HEADER:
            action = decrypt
        else:
            action = encrypt
    outdata = action(password, indata)
    outfile.write(outdata)
    if outfile is not stdout:
        outfile.close()

if __name__ == '__main__':
    main()
