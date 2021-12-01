from adafruit_servokit import ServoKit
from . import servo_controller_base, servo_map


class controller(servo_controller_base.controller):
    def __init__(self, servokit_channels=16):
        servo_controller_base.controller.__init__(self)
        self.mapping = servo_map.leg_servo_map()
        self.aux_mapping = servo_map.aux_servo_map()
        self.kit = ServoKit(channels=servokit_channels)

    def set_servokit_servo(self, s, v):
        if s == -1:
            return
        self.kit.servo[s].angle = clamp(v + 90, 0, 180)

    def _set_leg_servo(self, leg, joint, value):
        self.set_servokit_servo(self.mapping.get(leg, joint), value)

    def _set_aux_servo(self, name, value):
        self.set_servokit_servo(self.aux_mapping.get(name, -1), value)

    def _get_json(self):
        return {"legs": self.mapping.get_dict(), "aux": self.aux_mapping.get_dict()}

    def _set_json(self, d):
        self.mapping.set_dict(d["legs"])
        self.aux_mapping.set_dict(d["aux"])


def clamp(x, mi, ma):
    if x < mi: return mi
    if x > ma: return ma
    return x
