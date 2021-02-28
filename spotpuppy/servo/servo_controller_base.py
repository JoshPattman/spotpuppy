class controller:
    def __init__(self):
        self.servo_mapping = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        self.head_servo = -1
        self.tail_servo = -1
        self.servo_names = ["Hip", "Thigh", "Knee"]
    # Override this to change what happens when you set a legservo
    def set_servo(self, leg, joint, value):
        pass
    # Override this to change what happens when you set the head servo
    def set_head(self, value):
        pass
    # Override this to change what happens when you set the tail servo
    def set_tail(self, value):
        pass
    # Leave this as it is
    def set_all_servos(self, servos):
        for l in range(4):
            for j in range(3):
                self.set_servo(l, j, servos[l][j])
    def get_json(self):
        data = {"head":self.head_servo, "tail":self.tail_servo}
        data["legs"] = {}
        leg_names = ["FL", "FR", "BL", "BR"]
        for l in range(4):
            data["legs"][leg_names[l]] = {}
            data["legs"][leg_names[l]]["hip_Z"] = self.servo_mapping[l][0]
            data["legs"][leg_names[l]]["hip_X"] = self.servo_mapping[l][1]
            data["legs"][leg_names[l]]["knee"] = self.servo_mapping[l][2]
        return data
    def set_json(self, data):
        self.head_servo = data["head"]
        self.tail_servo = data["tail"]
        leg_names = ["FL", "FR", "BL", "BR"]
        for l in range(4):
            leg_mapping = [data["legs"][leg_names[l]]["hip_Z"], data["legs"][leg_names[l]]["hip_X"], data["legs"][leg_names[l]]["knee"]]
            self.servo_mapping[l] = leg_mapping