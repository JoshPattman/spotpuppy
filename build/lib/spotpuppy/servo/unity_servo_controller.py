from . import servo_controller_base
import os
import atexit

IS_IMPORTED = False

class controller(servo_controller_base.controller):
    def __init__(self, linked_sensor):
        global IS_IMPORTED
        if not IS_IMPORTED:
            global zmq
            import zmq
            IS_IMPORTED = True
        servo_controller_base.controller.__init__(self)
        self.linked_sensor = linked_sensor
        self.servos = []
        self.head = 0
        self.tail = 0

    def set_servo(self, leg, joint, value):
        self.servos[leg][joint] =  value

    def set_head(self, value):
        self.head = value

    def set_tail(self, value):
        self.tail = value

    def set_all_servos(self, servos, awaitUnity=True):
        servo_controller_base.controller.set_all_servos(self)
        if awaitUnity:
            self._await_unity_req()

    def _get_serialised(self):
        s = ""
        for leg in self.servos:
            i = 0
            for joint in leg:
                if i > 0:
                    s += ","
                s += str(joint)
                i+=1
            s += ";"
        s += str(self.head)
        return s
    def _await_unity_req(self):
        message = self.socket.recv().decode('utf-8')

        if message == "END_CONNECTION":
            os.exit(0)
        else:
            if not self.linked_sensor == None:
                try:
                    rots = message.split(",")
                    self.linked_sensor.x = range_rotation(float(rots[0]))
                    self.linked_sensor.z = range_rotation(float(rots[1]))
                except:
                    print("Could not read unity data stream (" + message + ")")
            self.socket.send(bytes(self._get_serialised(), 'utf-8'))
    def _end_unity_connection(self):
        message = self.socket.recv()
        self.socket.send(bytes("END_CONNECTION", 'utf-8'))

def range_rotation(r, begin=-180):
    while r > begin + 360:
        r -= 360
    while r < begin:
        r += 360
    return r