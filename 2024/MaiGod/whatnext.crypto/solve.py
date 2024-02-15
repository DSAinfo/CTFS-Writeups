#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes 

output = open('recurso/output.txt', 'r').readlines()

KEY = int(output[1].split("=")[1].strip())
enc = int(output[2].split("=")[1].strip())


print(long_to_bytes(KEY ^ enc).decode("utf-8"))