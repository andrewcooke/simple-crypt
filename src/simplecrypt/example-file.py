
from simplecrypt import encrypt, decrypt

from os.path import exists
from os import unlink


# this is an example program that reads and writes encrypted files.

# if the file "encrypted.txt" does not exist, then it is created with
# the contents "10 green bottles".

# if the file does exist, is is read, and the number of green bottles
# is reduced.  if there are no green bottles left, then the file is
# deleted, otherwise it is written with the new number.


PASSWORD = "secret"
FILENAME = "encrypted.txt"


def main():

    if exists(FILENAME):
        print("reading...")
        data = read_encrypted(PASSWORD, FILENAME)
        print("read %s from %s" % (data, FILENAME))
        n_bottles = int(data.split(" ")[0]) - 1
    else:
        n_bottles = 10
    
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
