import socket
from PIL import Image

from requests import ConnectTimeout

class mesmetronInterface:
    def __init__(self, host, port) -> None:
        self.port = port
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self) -> None:
        try:
            self.socket.setblocking(True)
            self.socket.connect((self.host, self.port))
                
        except ConnectionRefusedError:
            return 2
        except ConnectTimeout:
            return 3
        except ConnectionError:
            return 4
        except:
            return 5

        return 0


    def sendData(self, data) -> None:
        if len(data) != 1600:
            return 1
        try:
        
            self.socket.sendall(bytes(data))
                
        except ConnectionRefusedError:
            return 2
        except ConnectTimeout:
            return 3
        except ConnectionError:
            return 4
        except:
            return 5

        return 0

    def disconnect(self) -> None:
        self.socket.close()

class memsmetronPicture:
    def convertPicture(path):
        try:
            image = Image.open(path)
        except FileNotFoundError:
            return 2, None
        except:
            return 3, None
        pix = image.convert("RGB")

        if image.width != 200:
                print("Image is not 200 px wide. Image is instead " + image.width + "px wide! Can't convert!")
                return 1, None
        if image.height != 32:
                print("Image is not 32 px high. Image is instead " + image.height + "px high! Can't convert!")
                return 1, None

        data = []

        for y in range(32):
            for x in range(0, 200, 4):
                binout = 0x00
                color = pix.getpixel((x, y))
                r, g, b = color
                if r > 127:
                    binout = binout | 0b01000000
                if g > 127:
                    binout = binout | 0b10000000
                
                color = pix.getpixel((x + 1, y))
                r, g, b = color
                if r > 127:
                    binout = binout | 0b00010000
                if g > 127:
                    binout = binout | 0b00100000
                
                color = pix.getpixel((x + 2, y))
                r, g, b = color
                if r > 127:
                    binout = binout | 0b00000100
                if g > 127:
                    binout = binout | 0b00001000
                
                color = pix.getpixel((x + 3, y))
                r, g, b = color
                if r > 127:
                    binout = binout | 0b00000001
                if g > 127:
                    binout = binout | 0b00000010
                data.append(binout)
        return 0, data