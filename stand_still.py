from spotpuppy.models import basic_quaruped
from spotpuppy.servo import redboard_servo_controller

s = redboard_servo_controller.controller()
q = basic_quaruped.quadruped(servo_controller=s)

q.update()