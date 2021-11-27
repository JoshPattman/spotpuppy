import time

class max_ups:
    def __init__(self, target_ups):
        self.last = time.time()
        self.target_delay = 1/target_ups
    def update(self):
        t = time.time()
        dt = t-self.last
        sleep_time = self.target_delay - dt
        if sleep_time > 0:
            time.sleep(sleep_time)
        nt = time.time()
        ndt = nt-self.last
        self.last = nt
        return 1/ndt
