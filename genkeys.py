#!/usr/bin/env python3

import os
import sys


def gcd(a, b):
    while b != 0:
        tmp = b
        b = a % b
        a = tmp
    return a


def mod_pow(num, exp, mod):
    binary_exp = str(bin(exp))[2:]
    acc = 1
    y = num
    for digit in binary_exp[::-1]:
        if digit == '1':
            acc = (acc * y) % mod
        y = (y*y) % mod
    return acc % mod


def mod_inv(a, b):
    phi = b
    y = 0
    x = 1
    # extended euclidean algo
    while a > 1:
        quotient = a // b
        old_b = b
        b = a % b
        a = old_b
        old_y = y
        y = x - quotient * y
        x = old_y

    if x < 0:
        x += phi

    return x


# implementation of Miller-Rabin primality test
def is_prime(num, rounds=50):
    orig = num
    r = 0
    num -= 1
    while isinstance(num/2, int):
        num /= 2
        r += 1
    for i in range(rounds):
        rand_int = int.from_bytes(os.urandom(128), 'big') % (orig - 2)
        rand_int = rand_int if rand_int & 1 else rand_int + 1
        x = mod_pow(rand_int, num, orig)
        if x == 1 or x == orig-1:
            continue
        for _ in range(r):
            x = pow(x, 2) % orig
            if x == orig - 1:
                continue
        return False
    return True


def new_prime():
    prime = 0
    while not prime:
        num = int.from_bytes(os.urandom(128), 'big')
        num = num if num & 1 else num + 1
        if is_prime(num):
            prime = num
    return prime


def int_to_bytes(num):
    return num.to_bytes((num.bit_length() + 7) // 8, 'big')


def main():
    name = sys.argv[1]
    e = 65537
    p = e
    q = e
    n = 0
    phi_n = 0
    while gcd(e, p) != 1:
        p = new_prime()
        q = new_prime()
        n = p*q
        phi_n = (p-1)*(q-1)
    d = mod_inv(e, phi_n)

    with open('{}.pub'.format(name), 'w+') as pub:
        pub.write('{}\n'.format(int_to_bytes(n)))
        pub.write('{}\n'.format(int_to_bytes(e)))

    with open('{}.prv'.format(name), 'w+') as prv:
        prv.write('{}\n'.format(int_to_bytes(n)))
        prv.write('{}\n'.format(int_to_bytes(d)))


if __name__ == '__main__':
    main()
