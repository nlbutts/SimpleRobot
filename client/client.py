from inputs import get_gamepad
from threading import Thread, Lock
import struct
import socket
import time

UDP_IP = '192.168.4.1'
UDP_PORT = 5000

last_x = 0
last_y = 0
last_a = 0
last_b = 0
last_x
data = {"yaxis1": 0,
        "yaxis2": 0,
        "a": 0,
        "b": 0
        }

def tx_data(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        print(data)
        packed = struct.pack("iiii", data['yaxis1'], data['yaxis2'], data['a'], data['b'])
        sock.sendto(packed, (UDP_IP, UDP_PORT))
        time.sleep(0.05)

t1 = Thread(target=tx_data, args=(data,))
t1.start()

print('Started thread')

while True:
    events = get_gamepad()
    for event in events:
        if event.code == 'ABS_RY':
            #print(event.ev_type, event.code, event.state)
            data['yaxis1'] = int((event.state / 32768) * 4095)
        elif event.code == 'ABS_Y':
            #print(event.ev_type, event.code, event.state)
            data['yaxis2'] = int((event.state / 32768) * 4095)
        elif event.code == 'BTN_SOUTH':
            #print(event.ev_type, event.code, event.state)
            data['a'] = event.state
        elif event.code == 'BTN_EAST':
            #print(event.ev_type, event.code, event.state)
            data['b'] = event.state
        elif event.code == 'BTN_WEST':
            #print(event.ev_type, event.code, event.state)
            data['x'] = event.state
        elif event.code == 'BTN_NORTH':
            #print(event.ev_type, event.code, event.state)
            data['y'] = event.state


