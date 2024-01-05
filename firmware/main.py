from udp_rx import UDP_RX
from pca9685 import PCA9685
from machine import I2C, Pin, ADC
import time

i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=100000)
pca = PCA9685(i2c, 64)

udp = UDP_RX()

while True:
    time.sleep(0.1)
    data = udp.get()
    if data is not None:
        print(data)
        if data[2] == 0:
            pca.pwm(0, data[0])
            pca.pwm(1, data[0])
            pca.pwm(2, data[1])
            pca.pwm(3, data[1])
        else:
            pca.pwm(0, data[0])
            pca.pwm(1, -data[0])
            pca.pwm(2, data[1])
            pca.pwm(3, -data[1])

