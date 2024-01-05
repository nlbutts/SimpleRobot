import utime

class PID:
    def __init__(self, kp, ki, kd, minv, maxv):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.int_error = 0
        self.start = utime.ticks_us()
        self.prev_error = 0
        self.minv = minv
        self.maxv = maxv
        
    def process(self, error):
        self.stop = utime.ticks_us()
        diff = self.stop - self.start
        self.int_error += (error * diff / 1000000)
        der = (self.prev_error - error) / diff
        output = (self.kp * error) + (self.ki * self.int_error) + (self.kd * der)
        output = min(output, self.maxv)
        output = max(output, self.minv)
        self.prev_error = error
        self.start = self.stop
        return output
    
    def reset(self):
        self.start = utime.ticks_us()
        self.int_error = 0

