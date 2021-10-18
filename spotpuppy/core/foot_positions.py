# Experimental class for storing foot positions as abstract object not coordinate
# Will allow combining of different coordinate systems

import numpy as np

class foot_pos:
    def __init__(self, sh_pos = np.array([0,0,0]), sh_rot = np.array([0, 0])):
        self.sh_pos = sh_pos
        # [forward_backward, left_right]
        self.sh_rot = sh_rot
