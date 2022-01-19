#!/usr/bin/env bash


source venv/bin/activate

clear
echo "Files in directory:"
ls
echo
echo "Generating keys for alice"
./genkeys.py alice

echo
echo "Generating keys for bob"
./genkeys.py bob

echo
echo "Files in directory:"
ls
sleep 5

echo
echo "Contents of message1.txt:"
cat message1.txt
sleep 5
echo
echo
echo "Encrypting message1.txt into message1.cip with bob's key"
./crypt.py -e bob.pub message1.txt message1.cip
echo
echo "Contents of message1.cip:"
cat message1.cip
sleep 5
echo
echo
echo "Decrypting message1.cip into message1.txt with bob's key"
./crypt.py -d bob.prv message1.cip message1.txt
echo
echo "Contents of message1.txt:"
cat message1.txt
sleep 5


echo
echo
echo "Contents of message2.txt:"
cat message2.txt
sleep 5
echo
echo
echo "Encrypting message2.txt into message2.cip with alice's key"
./crypt.py -e alice.pub message2.txt message2.cip
echo
echo
echo "Contents of message2.cip:"
cat message2.cip
sleep 5
echo
echo
echo "Decrypting message2.cip into message2.txt with alice's key"
./crypt.py -d alice.prv message2.cip message2.txt
echo
echo "Contents of message2.txt:"
cat message2.txt
sleep 5
