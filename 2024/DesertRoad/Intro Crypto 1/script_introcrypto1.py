#!/usr/bin/env python
#CSCG

from pwn import xor #Makes it easier to xor
import re #regex

flag = bytes.fromhex("0904491eb7dc0f1d255721b1a1038e0db858ea2c873e63bb9ab9696965ba9116190a57dae20adda4cce5727c42f99bf3afc53875e483a6960be609c4a450de9a3ecbf9ceb6106048d7e1")

knownPlaintext = bytes.fromhex("F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1F1")
listCipherTexts = "ic1ListCT.txt" #list of ciphertexts

with open(listCipherTexts, 'r') as f:
    for line in range(256): #256 ciphertexts
        knownCiphertext = bytes.fromhex(f.readline()[16:]) #read the ciphertext in the line
        counterCiphertext = xor(knownPlaintext, knownCiphertext) # E(Counter) = ciphertext [xor] plaintext
        plainbytes = xor(flag, counterCiphertext) # plaintext = ciphertext [xor] E(Counter)
        if (re.search("CSCG", repr(plainbytes))): #Search for the format of the flag CSCG{}
                print(plainbytes)
                break
