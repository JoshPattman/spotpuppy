from . import servo_controller_base, servo_map
from . import redboard_modified_lib as redboard

class controller(servo_controller_base.controller):
    def __init__(self):
        self.mapping = servo_map.leg_servo_map()
        self.aux_mapping = servo_map.aux_servo_map()
        servo_controller_base.controller.__init__(self)

    def set_redboard_servo(self, s, v):
        if s == -1:
            return
        redboard.servo(s, v)

    def _set_leg_servo(self, leg, joint, value):
        self.set_redboard_servo(self.mapping.get(leg, joint))

    def _set_aux_servo(self, name, value):
        self.set_redboard_servo(self.aux_mapping.get(name, -1))

    def _get_json(self):
        return {"legs": self.mapping.get_dict(), "aux": self.aux_mapping.get_dict()}

    def _set_json(self, d):
        self.mapping.set_dict(d["legs"])
        self.aux_mapping.set_dict(d["aux"])