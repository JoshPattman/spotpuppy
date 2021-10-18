from . import leg_control, foot_positions
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
        self.foot_positions = [foot_positions.foot_pos(), foot_positions.foot_pos(), foot_positions.foot_pos(), foot_positions.foot_pos()]
        self.body_dims = body_dims

    def set_bone_length(self, bone_length):
        for l in range(4):
            self.legs[l].bone_length = bone_length
        self._recalc_resting_height()

    def _recalc_resting_height(self):
        l = self.legs[0].bone_length
        self.resting_height = math.sqrt(2 * (l * l))

    def set_leg(self, l, foot_position):
        self.foot_positions[l] = foot_position

    def set_all_legs(self, foot_positions):
        for i in range(4):
            self.set_leg(i, foot_positions[i])

    def update(self):
        for l in range(4):
            self.servo_rotations[l] = self.legs[l].calculate_servos(self.foot_positions[l].sh_pos)
            self.servo_rotations[l][0] += self.foot_positions[l].sh_rot[0]
            self.servo_rotations[l][1] += self.foot_positions[l].sh_rot[1]
