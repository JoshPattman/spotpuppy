"""
Allows the user to calculate servo positions of a 3 axis, 3 servo leg from coordinates

By Josh Pattman
"""


from math import degrees as rtod
import math
import numpy as np

# *************************Leg Math Functions************************

# returns the angle of a vector


def _degrees_2D(coord, dx, dy):
    if (coord[dy] == 0):
        coord[dy] = 0.000001
    val = rtod(math.atan(coord[dx] / coord[dy]))
    return val


# returns the angle that the knee servo should be at for a certain distance (pure angle)
def _knee_degrees(dist, bone_length):
    ratio = dist / (2 * bone_length)
    if ratio > 1:
        ratio = 1
    val = 0
    try:
        val = rtod(2 * math.asin(ratio))
    except:
        raise Exception("Position is out of range")
    return val

# returns the angle that the thigh should be at to counter the knee angle
def _counter_thigh_degrees(kd):
    return kd / 2


def _bound(a, mi, ma):
    if a < mi:
        return mi
    if a > ma:
        return ma
    return a


class _abstract_robot_leg:
    """Does trig calculations for an ideal leg, where a leg is resting when all servos are 0"""

    def __init__(self, bone_length, debugOOR=False):
        """
        Creates a new ARL

        Parameters
        ----------
            bone_length : float
                The length of each bone in the leg (distance from hip to knee or knee to foot)
            debugOOR : bool
                [Optional] If true a message will be printed if the leg is set to an out of range coordinate
        """
        self.l = bone_length
        self.debugOOR = debugOOR

    def calculate_angles(self, coord):
        """
        Calculates the angles of the three leg joints for this leg to move to a coordinate

        Parameters
        ----------
            coord : np.array dimension (3)
                The 3D coord to calculate for
        Returns
        -------
            angles : tuple length 3
                the rotations of each servo in the leg in order (hip_forward_backward, knee, hip_left_right)
        """
        dist = np.linalg.norm(coord)
        if dist > 2 * self.l:
            coord = coord * (1.999 * self.l / dist)
            if self.debugOOR:
                print("Coord was out of range so nomalised to %s" % coord)
        kd = _knee_degrees(dist, self.l)
        hd = _counter_thigh_degrees(kd) + _degrees_2D(coord, 0, 1)
        uhd = _degrees_2D(coord, 2, 1)
        return np.array([_bound(uhd, -90, 90), _bound(hd - 45, -90, 90), _bound(kd - 90, -90, 90)])


class robot_leg:
    """Adds tuning, reversing, and offset capability to an abstract_calculate_angles"""

    def __init__(self, bone_length=6, inverse_x=False, inverse_y=False, inverse_z=False, hip_offset=0, thigh_offset=0, knee_offset=0, reverse_knee=False, reverse_thigh=False):
        """
        Creates a new robot_leg

        Parameters
        ----------
        bone_length : float
            The length of each bone in the leg (distance from hip to knee or knee to foot)
        inverse_x : bool
            If true the X axis (forward/backward) will be reversed
        inverse_z : bool
            If true the Z axis (left/right) will be reversed
        hip_offset : float
            The amount in degrees to offset the hip_left_right servo
        thigh_offset : float
            The amount in degrees to offset the hip_forward_backward servo
        knee_offset : float
            The amount in degrees to offset the knee servo
        reverse_knee : bool
            If true the knee servo will be reversed
        reverse_thigh : bool
            If true the hip_forward_backward servo will be reversed
        """
        self.bone_length = bone_length

        self.inverse_x = inverse_x
        self.inverse_y = False  # inverse_y
        self.inverse_z = inverse_z

        self.thigh_offset = thigh_offset
        self.knee_offset = knee_offset
        self.hip_offset = hip_offset

        self.reverse_knee = reverse_knee
        self.reverse_thigh = reverse_thigh

        self.arl = _abstract_robot_leg(self.bone_length)

    def calculate_servos(self, coord):
        """
        Calculates the angles of the three leg servos for this leg to move to a coordinate

        Parameters
        ----------
        coord : np.array dimension (3)
            The 3D coordinate to calculate for

        Returns
        -------
        angles : list[3]
            The angles of the servos in form [hip_left_right, hip_forward_backward, knee], where 0 is centered
        """
        coord = np.copy(coord)
        if self.inverse_x:
            coord[1] = -coord[1]
        if self.inverse_z:
            coord[0] = -coord[0]
        # By default, at y=0 the foot is on the hip joint, and y=(2*bone_length) is the furthest point
        # Calculate the angles for an ideal robot leg
        baseAngles = self.arl.calculate_angles(coord)
        # Reverse servos is nescesary
        if self.reverse_thigh:
            baseAngles[1] = -baseAngles[1]
        if self.reverse_knee:
            baseAngles[2] = -baseAngles[2]
        # Add the offsets
        # Hip
        baseAngles[0] += self.hip_offset
        # Thigh
        baseAngles[1] += self.thigh_offset
        # Knee
        baseAngles[2] += self.knee_offset
        # Return
        return baseAngles
    def to_json_dict(self):
        """
        Returns a dict with the settings

        Returns
        -------
        settings : dict
            the settings form of this robot leg
        """
        return {"Inverse_Axis": {"X": self.inverse_x, "Y": self.inverse_y, "Z": self.inverse_z}, "Offsets": {"Hip_Z": self.hip_offset, "Hip_X": self.thigh_offset, "Knee": self.knee_offset}, "Reverse_Servo": {"Hip_X": self.reverse_thigh, "Knee": self.reverse_knee}}

    def load_json_dict(self, data):
        """
        Converts the dict with the settings into this robot leg

        Parameters
        ----------
        data : dict
            a dict generated by to_json_dict()
        """
        self.inverse_x = data["Inverse_Axis"]["X"]
        self.inverse_y = data["Inverse_Axis"]["Y"]
        self.inverse_z = data["Inverse_Axis"]["Z"]

        self.hip_offset = data["Offsets"]["Hip_Z"]
        self.thigh_offset = data["Offsets"]["Hip_X"]
        self.knee_offset = data["Offsets"]["Knee"]

        self.reverse_thigh = data["Reverse_Servo"]["Hip_X"]
        self.reverse_knee = data["Reverse_Servo"]["Knee"]
