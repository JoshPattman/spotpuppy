from ..core import quadruped_controller
from ..servo import servo_controller_base
from ..rotation import rotation_sensor_base
import math
from ..utils import json_serialiser as js
import numpy as np
from scipy.spatial.transform import Rotation as R

class quadruped:
    def __init__(self, rotation_sensor=None, servo_controller=None, bone_length=6, body_dims=[10, 10], fall_rotation_limit=0):
        self.quad_controller = quadruped_controller.quadruped_controller(bone_length, body_dims)
        # If not specified, set the servo controller or rotation sensor to the base class so the will have no functionality but still not break the code
        if servo_controller == None:
            self.servo_controller = servo_controller_base.controller()
        else:
            self.servo_controller = servo_controller
        if rotation_sensor == None:
            self.rotation_sensor = rotation_sensor_base.sensor()
        else:
            self.rotation_sensor = rotation_sensor
        # If this is zero the it will never detect that it has fallen over
        self.set_rotation_limit(fall_rotation_limit)
        self.current_rotation = np.array([0, 0])


    def set_rotation_limit(self, limit):
        limit = 0 if limit < 0 else limit
        self.fall_rotation_limit = limit
        self.cos_fall_rotation_limit = math.cos(math.radians(limit))

    def check_is_fallen_over(self):
        if self.fall_rotation_limit == 0:
            return False
        rot = self.current_rotation
        if math.cos(math.radians(rot[0]) < self.cos_rotation_limit or math.cos(math.radians(rot[1])) < self.cos_rotation_limit):
            return True
        return False

    def get_dir(self, dir_name):
        return self.quad_controller.directions[dir_name]()

    def update(self):
        # Rotation update
        if not self.rotation_sensor == None:
            self.rotation_sensor.update()
            roll_pitch = self.rotation_sensor.get_angle()
            self.current_rotation = R.from_euler('xz', roll_pitch, degrees=True)

        # tell the underlying quad controller what rotation we are at
        self._on_set_rotation()

        # This is where functionality is added
        self._on_update()

        # Update desired servos
        self.quad_controller.update_servos()
        # Update physical servos
        if not self.servo_controller == None:
            self.servo_controller.set_all_servos(self.quad_controller.servo_rotations)

    # Override this to change what rotation the quad controller thinks we are at
    def _on_set_rotation(self):
        self.quad_controller.body_rotation = self.current_rotation

    # Override this and use quad_controller.set_servo to set a servo. The servos do not update instantly, but after when this function returns
    def _on_update(self):
        # Set all legs to default height
        posses = self._calculate_still_positions()
        for l in range(4):
            self.quad_controller.set_leg(l, posses[l])

    def get_json_dict(self):
        json_dict = {}
        json_dict["body_dims"] = js.vec_2_to_json(self.quad_controller.body_dims)
        json_dict["bone_length"] = self.quad_controller.get_bone_length()
        json_dict["fall_rotation_limit"] = self.fall_rotation_limit
        json_dict["class_parameters"] = self._get_custom_json_params()
        return json_dict
    def set_json_dict(self, json_dict):
        self.quad_controller.body_dims = js.json_to_vec_2(json_dict["body_dims"])
        self.quad_controller.set_bone_length(json_dict["bone_length"])
        self.fall_rotation_limit = json_dict["fall_rotation_limit"]
        self._set_custom_json_params(json_dict["class_parameters"])

    # Override this to add custom save information
    def _get_custom_json_params(self):
        return {}
    def _set_custom_json_params(self, json_dict):
        pass

    # Calculate positions of the legs when they are at their default positions
    def _calculate_still_positions(self):
        dh = self.quad_controller.resting_height
        localRestingPos = np.array([0, dh, 0])
        posses = np.array([localRestingPos,localRestingPos,localRestingPos,localRestingPos])
        return posses