import time

class pid_controller:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.last_error = 0
        self.integral = 0
        self.reset_time()

        self.target = 0

    def update(self, val):
        t = time.time()
        dt = t - self.last_time
        self.last_time = t

        error = self.target - val
        d = (error - self.last_error) / dt
        self.integral += error * dt
        self.last_error = error

        return (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * d)

    def reset_time(self):
        self.last_time = time.time()

    def set_target(self, target):
        self.target = target