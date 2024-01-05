# SPDX-FileCopyrightText: 2022 Jamon Terrell <github@jamonterrell.com>
# SPDX-License-Identifier: MIT

from rp2 import PIO, StateMachine, asm_pio
from machine import Pin, PWM
import utime
import math

@asm_pio(autopush=True, push_thresh=32)
def encoder():
    label("start")
    wait(0, pin, 0)         # Wait for CLK to go low
    jmp(pin, "WAIT_HIGH")   # if Data is low
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop1")
    label("nop1")
    mov(x, invert(x))
    label("WAIT_HIGH")      # else
    jmp(x_dec, "nop2")          # Decrement X
    label("nop2")

    wait(1, pin, 0)         # Wait for CLK to go high
    jmp(pin, "WAIT_LOW")    # if Data is low
    jmp(x_dec, "nop3")          # Decrement X
    label("nop3")

    label("WAIT_LOW")       # else
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop4")
    label("nop4")
    mov(x, invert(x))
    wrap()

@asm_pio(autopush=True, push_thresh=32)
def foo():
    label("start")
    wait(0, pin, 0)         # Wait for CLK to go low

class Encoders():
    def __init__(self):
        self.sm2pin = [[0, 1],
                       [2, 3],
                       [4, 5],
                       [6, 7],
                       [8, 9],
                       [10, 11],
                       [17, 18],
                       [19, 20]]

        self.encs = []
        self.encs.append(self.createNewSM(0))
        self.encs.append(self.createNewSM(1))
        self.encs.append(self.createNewSM(2))
        self.encs.append(self.createNewSM(3))
        #self.encs.append(self.createNewSM(4))
        self.encs.append(None)
        self.encs.append(self.createNewSM(5))
        self.encs.append(self.createNewSM(6))
        self.encs.append(self.createNewSM(7))

        self.reset()
        self.enableAll()

    def createNewSM(self, num: int):
        pin1 = self.sm2pin[num][0]
        pin2 = self.sm2pin[num][1]
        print(f'Attempting to configure sm {num} with pins: {pin1} {pin2}')
        return StateMachine(num, encoder, freq=125_000_000, in_base=Pin(pin1, pull=Pin.PULL_UP), jmp_pin=Pin(pin2, pull=Pin.PULL_UP))

    def pos(self, num: int) -> int:
        temp = 0
        enc = self.encs[num]
        if enc is not None:
            self.encs[num].exec("in_(x, 32)")
            temp = self.encs[num].get()
            if temp > pow(2, 31):
                return temp - pow(2,32)
        return temp

    def reset(self, motor=-1):
        if motor == -1:
            for enc in self.encs:
                if enc is not None:
                    enc.exec("set(x, 0)")
        else:
            enc = self.encs[motor]
            if enc is not None:
                enc.exec("set(x, 0)")
                
    def enableAll(self):
        for enc in self.encs:
            if enc is not None:
                enc.active(1)
    
    def printPos(self):
        s = ''
        for i in range(8):
            s += f'{self.pos(i)}, '
        print(s)