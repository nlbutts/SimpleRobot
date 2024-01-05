from machine import I2C, Pin
from pid import PID
import time
import struct 

class DriveMotor:
    def __init__(self, drive_motors: list, pca, encoders):
        """Initialize the drive motors

        Param:
            drive_motors: list of numbers indicating the four drive motors
            pca: The PCA PWM Controller
            encoders: The rotary encoders input
        """
        self.drive_motors = drive_motors
        if len(drive_motors) != 4:
            raise Exception("Expected 4 drive motors")
        self.pca = pca
        self.encoders = encoders

    def set(self, speed):
        """
        Control the drive motors.

        param:
            speed: -4095 to +4095
        """
        for motor in self.drive_motors:
            self.pca.pwm(motor, speed)

    def getPos(self, motor):
        return self.encoders.pos(self.drive_motors[motor])

    def reset(self):
        for motor in self.drive_motors:
            self.encoders.reset(motor)

