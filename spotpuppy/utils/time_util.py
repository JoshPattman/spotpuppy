import time

class timer:
    def __init__(self):
        self.t = time.perf_counter()
    def stop(self):
        self.time = time.perf_counter() - self.t
    def __repr__(self):
        return str(self.time)
class max_ups:
    def __init__(self, target_ups):
        self.last = time.perf_counter()
        self.target_delay = 1/target_ups
    def update(self):
        t = time.perf_counter()
        dt = t-self.last
        sleep_time = self.target_delay - dt
        if sleep_time > 0:
            time.sleep(sleep_time)
        self.last = time.perf_counter()
