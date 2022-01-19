# RSA Implementation

04/08/2021

Python version 3.6+

What Is This?
-------------
This is a simple RSA implementation that is used to encrypt and decrypt an AES key. Additionally, there is a function to generate 1024 bit keys with high-confidence using the Miller-Rabin primality test.

How To Use This
---------------
1. Install the necessary requirements with `pip install -r requirements`
2. Give test.sh permission to execute with `chmod +x test.sh`
3. Run (and/or modify) test.sh with `./test.sh`


Explanation
---------------
The design of each of the programs is very simple.

In genkeys.py, I first try to find two 1024-bit prime numbers. To do this, I generate 1024-bit numbers with os.urandom() and test primality. I implemented the Miller-Rabin primality test to do this, which seems to be one of the faster practical primality tests out there. Next, I get the mod inverse of e (65537) and phi(n) to get d. I used the extended Euclidean algorithm for this. Next, I simply write n on one line of the public key file and e on the next line, and then I write n on one line of the private key file and d on the next line. There are sometimes I need to convert integers to and from byte strings like when testing primality and doing gcd, so I convert one to the other either in a function or in-line.

In crypt.py, under encryption, 16 random bytes (128 bits) are generated for the AES key. Then a copy of that AES key is encrypted with the RSA public key taken from the public key file. The encrypted AES key is then put at the beginning of the soon-to-be encrypted file (~256 bits long). The plaintext file is then encrypted with the original AES key and stored in the encrypted file beginning at byte 256.

Under decryption, the first 256 bytes of the encrypted file are extracted from the file to form the encrypted AES key. The AES key is then decrypted with the private key found in the private key file. It’s the same as encryption but with the ciphertext and decryption key: c^d mod n. With the AES key, it’s trivial to decrypt the encrypted file starting at byte position 256.

