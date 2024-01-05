from machine import I2C, Pin
import struct
import binascii
import time

class PCAConfig():
    COAST = 0
    BRAKE = 1

class PCA9685():
    def __init__(self, i2c: I2C, addr: int, cfg=PCAConfig.BRAKE):
        """PCA9685 PWM Device.

        Param:
            i2c: i2c bus that this device lives on
            addr: address of this device
            cfg: Run in brake or coast mode
        """
        self.i2c = i2c
        self.addr = addr

        # Enable sleep mode
        self.i2c.writeto_mem(addr, 0, bytes([0x10]))
        # Set prescaler to something faster
        self.i2c.writeto_mem(addr, 0xFE, bytes([0x0F]))
        # Put into normal mode with auto inc
        self.i2c.writeto_mem(addr, 0, bytes([0x20]))
        # Enable INVRT bit and OUTDRV
        self.i2c.writeto_mem(addr, 1, bytes([0x14]))

        self.cfg = []

        for i in range(8):
            if cfg == PCAConfig.BRAKE:
                self.brake(i)
            else:
                self.coast(i)
            self.cfg.append(cfg)

    def configure(self, motor: int, cfg: PCAConfig):
        """Configure the motor

        Param:
            motor: The motor to control 0 to 7
        """
        self.cfg[motor] = cfg

    def pwm(self, motor: int, dc: int):
        """Set the PWM of the motor

        Param:
            motor: The motor to control 0 to 7
            dc: The duty cycle from -4095 to 4095
        """
        offset = (8 * (motor)) + 6
        dc = min(dc, 4095)
        dc = max(dc, -4095)

#         if dc > 4095:
#             dc = 4095
#         elif dc < -4095:
#             dc = -4095

        if dc > 0:
            data = [dc, 0, 4096, 0]
        elif dc < 0:
            dc = -dc
            data = [4096, 0, dc, 0]
        else:
            if self.cfg[motor] == PCAConfig.COAST:
                #print('Setting coast')
                data = [4096, 0, 4096, 0]
            else:
                #print('Setting brake')
                data = [0, 4096, 0, 4096]

        bindata = struct.pack('<HHHH', data[0], data[1], data[2], data[3])

        self.i2c.writeto_mem(self.addr, offset, bindata)

    def coast(self, motor):
        """Set the motor to coast mode

        Param:
            motor: The motor to control 0 to 7
        """
        offset = (8 * (motor)) + 6
        bindata = struct.pack('<HHHH', 0, 0, 0, 0)
        self.i2c.writeto_mem(self.addr, offset, bindata)

    def brake(self, motor):
        """Set the motor to brake mode

        Param:
            motor: The motor to control 0 to 7
        """
        offset = (8 * (motor)) + 6
        bindata = struct.pack('<HHHH', 4096, 0, 4096, 0)
        self.i2c.writeto_mem(self.addr, offset, bindata)

