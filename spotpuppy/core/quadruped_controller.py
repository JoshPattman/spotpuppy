from . import leg_control
import math
import numpy as np

class quadruped_controller:
    def __init__(self, bone_length, body_dims):
        self.legs = []
        for l in range(4):
            self.legs.append(leg_control.robot_leg(bone_length=bone_length))
        self._recalc_resting_height()
        self.body_rotation = np.array([0, 0])
        self.servo_rotations = np.zeros(shape=(4, 3))
        # These are in leg space
        self.foot_positions = np.zeros(shape=(4, 3))
        self.body_dims = body_dims
        self.FL_relative_multipliers = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])

    def set_bone_length(self, bone_length):
        for l in range(4):
            self.legs[l].bone_length = bone_length
        self._recalc_resting_height()

    def _recalc_resting_height(self):
        self.resting_height = math.sqrt(2 * (l * l))

    def _calc_FL_vert_shoulder_offsets(self):
        sin_rots = np.array([math.sin(math.radians(rot)) for rot in self.body_rotation])
        return (self.body_dims/2) * sin_rots

    def _calc_FL_horiz_shoulder_offsets(self):
        cos_rots = np.array([math.cos(math.radians(rot)) for rot in self.body_rotation])
        half_dims = (self.body_dims/2)
        return (half_dims * cos_rots - half_dims)/2

    def set_leg(l, pos):
        self.foot_positions[l] = pos

    def update(self):
        v_shoulder_off = self._calc_FL_vert_shoulder_offsets()
        h_shoulder_off = self._calc_FL_horiz_shoulder_offsets()
        for l in range(4):
            l_v_shoulder_off = self.FL_relative_multipliers[l] * v_shoulder_off
            l_y_shoulder_off = np.array([0, np.sum(l_v_shoulder_off), 0])
            l_h_shoulder_off = self.FL_relative_multipliers[l] * h_shoulder_off
            l_xy_shoulder_off = np.array([l_h_shoulder_off[0], 0, l_h_shoulder_off[1]])
            self.servo_rotations[l] = self.legs[l].calculate_servos(self.foot_positions[l] + l_y_shoulder_off + l_xy_shoulder_off)