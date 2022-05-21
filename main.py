#!/usr/bin/python3

import socket
import spidev

#speed = 15200
speed = 976000
#speed = 31200000

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = speed
spi.mode = 0b00

# For future reference to DATA register on FPGA
# spi.xfer([0b11110010])

HOST = "0.0.0.0"    # Bind address
PORT = 5000         # Port to listen to

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                count = 0
                data = conn.recv(2048)
                if not data:
                    break
                if len(data) != 1600:
                    break
                formatted = [None] * 1600
                cnt = 0
                for y in range(7, -1 ,-1):
                    for x in range(49, -1, -1):
                        for b in range(4):
                            bitmask = 0
                            pix0, pix1, pix2, pix3 = 0, 0, 0, 0
                            match b:
                                case 0:
                                    bitmask = 0b00000011
                                    pix0 = (data[x+50*y] & bitmask) << 6
                                    pix1 = (data[(x+50*y) + 400] & bitmask) << 4
                                    pix2 = (data[(x+50*y) + 800] & bitmask) << 2
                                    pix3 = (data[(x+50*y) + 1200] & bitmask)
                                case 1:
                                    bitmask = 0b00001100
                                    pix0 = (data[(x+50*y)] & bitmask) << 4
                                    pix1 = (data[(x+50*y) + 400] & bitmask) << 2
                                    pix2 = (data[(x+50*y) + 800] & bitmask)
                                    pix3 = (data[(x+50*y) + 1200] & bitmask) >> 2
                                case 2:
                                    bitmask = 0b00110000
                                    pix0 = (data[(x+50*y)] & bitmask) << 2
                                    pix1 = (data[(x+50*y) + 400] & bitmask)
                                    pix2 = (data[(x+50*y) + 800] & bitmask) >> 2
                                    pix3 = (data[(x+50*y) + 1200] & bitmask) >> 4
                                case 3:
                                    bitmask = 0b11000000
                                    pix0 = (data[(x+50*y)] & bitmask)
                                    pix1 = (data[(x+50*y) + 400] & bitmask) >> 2S
                                    pix2 = (data[(x+50*y) + 800] & bitmask) >> 4
                                    pix3 = (data[(x+50*y) + 1200] & bitmask) >> 6
                                case _:
                                    bitmask = 0b00000000
                                    pix0 = 0b00000011
                                    pix1 = 0b00001100
                                    pix2 = 0b00110000
                                    pix3 = 0b11000000

                            formatted[cnt] = (pix0 | pix1 | pix2 | pix3)
                            cnt = cnt + 1
                for x in formatted:
                    spi.xfer([x])
                print("New frame send!")