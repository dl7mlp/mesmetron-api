#!/usr/bin/python3
from mesmetronInterface import mesmetronInterface, memsmetronPicture
import sys
import time

from requests import ConnectTimeout

host = "94.45.239.116"  # The server's hostname or IP address
port = 5000  # The port used by the server

code, data1 = memsmetronPicture.convertPicture(sys.argv[1])

if code != 0:
    exit(1)

code, data2 = memsmetronPicture.convertPicture(sys.argv[2])

if code != 0:
    exit(1)

while True:

    con = mesmetronInterface(host, port)

    code = con.connect()

    if code != 0:
        exit(2)
    print("(Re)connect")

    while True:
        if con.sendData(data1) != 0:
            break
        time.sleep(float(sys.argv[3]))
        if con.sendData(data2) != 0:
            break
        time.sleep(float(sys.argv[3]))