class controller:
    def __init__(self):
        pass

    # Override this to change what happens when you set a leg servo
    def _set_leg_servo(self, leg, joint, value):
        pass

    # Leave this as it is
    def set_all_leg_servos(self, servos):
        for l in range(4):
            for j in range(3):
                self._set_leg_servo(l, j, servos[l][j])

    def set_aux_servo(self, name, value):
        self._set_aux_servo(name, value)

    # Override this to change what happens when you set a aux servo
    def _set_aux_servo(self, name, value):
        pass

    def _get_json(self):
        return {}

    def _set_json(self, data):
        pass

    def get_json(self):
        return self._get_json()

    def set_json(self, data):
        self._set_json(data)
