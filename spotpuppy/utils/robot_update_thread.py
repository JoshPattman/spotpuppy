import threading
from . import time_util
import time


# One slight problem here is that time.time() precision is to 16 ms on windows (slow) as opposed to 1 ms on
# linux and mac (much better). Moral of the story: SWITCH TO LINUX
def _update_thread(robot, max_update_per_sec, warn_if_low_threshold):
    max_ups = time_util.max_ups(max_update_per_sec)
    while True:
        robot.update()
        ups = max_ups.update()
        if ups < warn_if_low_threshold:
            print("Warning, UPS at",ups)


def start_threaded_updates(robot, max_update_per_sec=50, warn_if_low=False):
    # If we ask it to, this will warn the user when updates per second drops below 90% of what it should be
    wilt = max_update_per_sec * 2
    if warn_if_low:
        wilt = max_update_per_sec - (0.1*max_update_per_sec)
    # Set daemon=True so that the thread quits when our program exits
    t = threading.Thread(target=_update_thread, args=(robot, max_update_per_sec, wilt), daemon=True)
    t.start()
    return t
