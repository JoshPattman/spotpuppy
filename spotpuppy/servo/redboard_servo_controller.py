from . import servo_controller_base

IS_IMPORTED=False

class controller(servo_controller_base.controller):
    def __init__(self):
        global IS_IMPORTED
        if not IS_IMPORTED:
            global redboard
            from . import redboard_modified_lib as redboard
            IS_IMPORTED = True
        servo_controller_base.controller.__init__(self)

        def set_servo(self, leg, joint, value):
            svo_num = self.servo_mapping[leg][joint]
            if svo_num == -1:
                return
            redboard.servo(svo_num, value)

        def set_head(self, value):
            if self.head_servo == -1:
                return
            redboard.servo(self.head_servo, value)

        def set_tail(self, value):
            if self.tail_servo == -1:
                return
            redboard.servo(self.tail_servo, value)