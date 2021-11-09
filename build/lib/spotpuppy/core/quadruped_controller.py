from . import leg_control
import math
import numpy as np
from scipy.spatial.transform import Rotation as R

class quadruped_controller:
    def __init__(self, bone_length, body_dims):
        self.legs = []
        for l in range(4):
            self.legs.append(leg_control.robot_leg(bone_length=bone_length))
        self._recalc_resting_height()
        self.body_rotation = R.from_euler('xz', [0,0], degrees=True)
        self.servo_rotations = np.zeros(shape=(4, 3))
        # These are in leg space
        self.foot_positions = [np.array([0,0,0]), np.array([0,0,0]), np.array([0,0,0]), np.array([0,0,0])]
        self.body_dims = body_dims
        self.directions = {
            "body.forward": lambda: np.array([1, 0, 0]),
            "body.down": lambda: np.array([0, 1, 0]),
            "body.left": lambda: np.array([0, 0, 1]),
            "global.down": lambda: self.body_rotation.apply(np.array([0, 1, 0])),
            "global.forward": lambda: self.body_rotation.apply(np.array([1, 0, 0])),
            "global.left": lambda: self.body_rotation.apply(np.array([0, 0, 1]))
        }

    def get_vector_to_robot_center(self, leg_index, coord_system):
        X = self.body_dims[0] * self.directions[coord_system+".forward"]()*0.5
        Z = self.body_dims[1] * self.directions[coord_system+".left"]()*0.5
        if leg_index == 0:
            return (-X) + (-Z)
        elif leg_index == 1:
            return (-X) + Z
        elif leg_index == 2:
            return X + (-Z)
        elif leg_index == 3:
            return X + Z

    def set_bone_length(self, bone_length):
        for l in range(4):
            self.legs[l].bone_length = bone_length
        self._recalc_resting_height()

    def get_bone_length(self):
        return self.legs[0].bone_length

    def _recalc_resting_height(self):
        l = self.get_bone_length()
        self.resting_height = math.sqrt(2 * (l * l))

    def set_leg(self, l, foot_position):
        self.foot_positions[l] = foot_position

    def set_all_legs(self, foot_positions):
        for i in range(4):
            self.set_leg(i, foot_positions[i])


    def update_servos(self):
        for l in range(4):
            self.servo_rotations[l] = self.legs[l].calculate_servos(self.foot_positions[l])