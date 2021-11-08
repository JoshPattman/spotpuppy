from . import rotation_sensor_base
import serial

class sensor(rotation_sensor_base.sensor):
    def __init__(self, inverse_x=False, inverse_z=False, serial_port="/dev/ttyUSB0"):
        rotation_sensor_base.sensor.__init__(self, inverse_x=inverse_x, inverse_z=inverse_z)
        self.serial_port = serial_port
        self.s = serial.Serial("/dev/ttyUSB0", 115200)
        while self.s.readline() != b"READY\r\n":
            pass

    def calibrate(self):
        self.s.write(b"c")
        while self.s.readline() != b"READY\r\n":
            pass

    def update(self):
        self.s.write(b"r")
        rotation_string = self.s.readline().decode('utf-8').strip()
        if rotation_string[0] == "D":
            rotation_string = rotation_string[1:]
            rotations_string = rotation_string.split(",", -1)
            self.rotation[0] = float(rotations_string[0])
            self.rotation[1] = float(rotations_string[1])
