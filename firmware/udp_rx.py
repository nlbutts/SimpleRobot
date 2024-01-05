import network
import socket
import time
import struct

class UDP_RX():
    def __init__(self):
        ssid = "PicoW"
        password = "123456789"

        ap = network.WLAN(network.AP_IF)
        ap.config(essid=ssid, password=password) 
        ap.active(True)

        while ap.active == False:
          pass

        print("Access point active")
        print(ap.ifconfig())

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.1)

        server_address = ('', 5000)
        self.sock.bind(server_address)

        buf_size = 4096
        self.buf = bytearray(buf_size)

    def get_ip(self):
        """Returns the current IP address."""
        return self.ip_addr

    def get(self):
        """Get the UDP data.
        The format of the data is
        xaxis_drive, yaxis_drive, xaxis_swerve, yaxis_swerve, buttons

        The Buttons is a bit field defined as follows:
        Bit 0 = A
        Bit 1 = B
        Bit 2 = X
        Bit 3 = Y
        """
        try:
            buf, client_address = self.sock.recvfrom(20)
            message = struct.unpack('iiii', buf)
            return message
        except Exception:
            pass

        return None

    