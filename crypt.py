#!/usr/bin/env python3

import ast
import os
import sys

import pyaes


def mod_pow(num, exp, mod):
    binary_exp = str(bin(exp))[2:]
    acc = 1
    y = num
    for digit in binary_exp[::-1]:
        if digit == '1':
            acc = (acc * y) % mod
        y = (y*y) % mod
    return acc % mod


def get_key_from_in_file(in_file):
    buf = b''
    with open(in_file, 'rb') as f:
        for i in range(256):
            buf += f.read(1)
    return buf


def encrypt_file(key, input_file, output_file):
    aes = pyaes.AESModeOfOperationCTR(key)
    in_file = open(input_file, 'rb')
    out_file = open(output_file, 'ab+')
    out_file.seek(256)
    pyaes.encrypt_stream(aes, in_file, out_file)
    in_file.close()
    out_file.close()


def decrypt_file(key, input_file, output_file):
    aes = pyaes.AESModeOfOperationCTR(key)
    in_file = open(input_file, 'rb')
    in_file.seek(256)
    out_file = open(output_file, 'wb')
    pyaes.decrypt_stream(aes, in_file, out_file)
    in_file.close()
    out_file.close()


def encrypt_key(key, key_file):
    with open(key_file, 'r') as f:
        text = f.readlines()

    n = bytes_to_int(ast.literal_eval(text[0]))
    e = bytes_to_int(ast.literal_eval(text[1]))
    m = bytes_to_int(key)

    ciphertext = int_to_bytes(mod_pow(m, e, n))
    return ciphertext


def decrypt_key(enc_key, key_file):
    with open(key_file, 'r') as f:
        text = f.readlines()

    n = bytes_to_int(ast.literal_eval(text[0]))
    d = bytes_to_int(ast.literal_eval(text[1]))
    c = bytes_to_int(enc_key)

    message = int_to_bytes(mod_pow(c, d, n))
    return message


def add_key_to_file(out_file, key):
    open(out_file, 'wb+').write(key)


def int_to_bytes(num):
    return num.to_bytes((num.bit_length() + 7) // 8, 'big')


def bytes_to_int(bytes):
    return int.from_bytes(bytes, 'big')


def main():
    enc = True if sys.argv[1] == '-e' else False
    key_file = sys.argv[2]
    input_file = sys.argv[3]
    output_file = sys.argv[4]

    if enc:
        key = os.urandom(16)
        enc_key = encrypt_key(key, key_file)
        add_key_to_file(output_file, enc_key)
        encrypt_file(key, input_file, output_file)
    else:
        enc_key = get_key_from_in_file(input_file)
        key = decrypt_key(enc_key, key_file)
        decrypt_file(key, input_file, output_file)


if __name__ == '__main__':
    main()
