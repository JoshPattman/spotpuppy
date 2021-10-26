from adafruit_servokit import ServoKit
from . import servo_controller_base

class controller(servo_controller_base.controller):
    def __init__(self, servokit_channels=16):
        servo_controller_base.controller.__init__(self)
        self.kit = ServoKit(channels=servokit_channels)

    def set_servo(self, leg, joint, value):
        svo_num = self.servo_mapping[leg][joint]
        if svo_num == -1:
            return
        self.kit.servo[svo_num].angle = value + 90

    def set_head(self, value):
        if self.head_servo == -1:
            return
        self.kit.servo[self.head_servo].angle = value + 90

    def set_tail(self, value):
        if self.tail_servo == -1:
            return
        self.kit.servo[self.tail_servo].angle = value + 90