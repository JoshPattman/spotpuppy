class leg_servo_map:
    def __init__(self):
        self.leg_names = ["FL", "FR", "BL", "BR"]
        self.joint_names = ["hip_Z", "hip_X", "knee"]
        self.mapping = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]

    def get(self, leg, joint):
        return self.mapping[leg][joint]

    def set_dict(self, d):
        for l in range(4):
            leg_mapping = []
            for j in range(3):
                leg_mapping.append(d[self.leg_names[l]][self.joint_names[j]])
            self.mapping[l] = leg_mapping

    def get_dict(self):
        data = {}
        for l in range(4):
            data[self.leg_names[l]] = {}
            for j in range(3):
                data[self.leg_names[l]][self.joint_names[j]] = self.mapping[l][j]
        return data


class aux_servo_map:
    def __init__(self):
        self.mapping = {}

    def get(self, name, default):
        if name in self.mapping:
            return self.mapping[name]
        return default

    def get_dict(self):
        return self.mapping

    def set_dict(self, d):
        self.mapping = d
