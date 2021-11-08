import numpy as np

class sensor:
    def __init__(self, inverse_x=False, inverse_z=False):
        self.inverse_x = inverse_x
        self.inverse_z = inverse_z
        self.rotation = np.array([0, 0])
    def get_angle(self):
        rot = np.copy(self.rotation)
        if self.inverse_x:
            rot[0] = -rot[0]
        if self.inverse_z:
            rot[1] = -rot[1]
        return rot
    # Override update to add functionality
    def update(self):
        pass
    # Override update to add the ability to calibrate
    def calibrate(self):
        pass