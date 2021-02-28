from . import rotation_sensor_base

class sensor(rotation_sensor_base.sensor):
    def __init__(self, inverse_x=False, inverse_z=False, show_console_debug=False):
        rotation_sensor_base.sensor.__init__(self, inverse_x=inverse_x, inverse_z=inverse_z)
        self.show_console_debug = show_console_debug
    def update(self):
        if self.show_console_debug:
            print("Current angle is %s"%self.rotation)