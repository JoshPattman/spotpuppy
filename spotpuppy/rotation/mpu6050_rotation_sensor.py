from math import atan, sqrt, pow, radians, degrees
from . import rotation_sensor_base

IS_IMPORTED=False

class sensor(rotation_sensor_base.sensor):
    def __init__(self, inverse_x=False, inverse_z=False, accelerometer_bias=0.05):
        global IS_IMPORTED
        if not IS_IMPORTED:
            global mpu6050
            from mpu6050 import mpu6050
            IS_IMPORTED = True
        rotation_sensor_base.sensor.__init__(self, inverse_x=inverse_x, inverse_z=inverse_z)
        self.accelerometer_bias=accelerometer_bias
        self.mpu = mpu6050(0x68)
        self.rotation[0] = 0
        self.rotation[1] = 0
        self.dx = 0
        self.dy = 0
        self.ax = 0
        self.ay = 0
        self.last_update = time.time()

    def update(self):
        # Get gyro data
        data = self.mpu.get_gyro_data()
        # Find elapsed time
        t = time.time()
        elaplsed = t - self.last_update
        self.last_update = t
        # Add the rotation velocity * time
        self.rotation[0] += (data['x'] - self.dx) * elaplsed
        self.rotation[1] += (data['y'] - self.dy) * elaplsed
        # Get accel angle
        aang = self._get_acc_ang()
        # Add accel angle into the actual angle (slowly introducing it to reduce noise, as it is only really used to stop gyro drift)
        self.rotation[0] = (self.rotation[0] * (1 - self.accelerometer_bias)) + (aang[0] * self.accelerometer_bias)
        self.rotation[1] = (self.rotation[1] * (1 - self.accelerometer_bias)) + (aang[1] * -self.accelerometer_bias)

    def calibrate(self):
        data1 = self.mpu.get_gyro_data()
        time.sleep(0.5)
        data2 = self.mpu.get_gyro_data()
        time.sleep(0.5)
        data3 = self.mpu.get_gyro_data()
        self.dx = (data1['x'] + data2['x'] + data3['x']) / 3
        self.dy = (data1['y'] + data2['y'] + data3['y']) / 3
        self.ax = 0
        self.ay = 0
        adata = self._get_acc_ang()
        self.ax = adata[0]
        self.ay = adata[1]
        self.rotation[0] = 0
        self.rotation[1] = 0

    def _get_acc_ang(self):
        data = self.mpu.get_accel_data()
        ax = data['y']
        ay = data['x']
        az = data['z']
        xAngle = degrees(atan(ax / (sqrt(pow(ay, 2) + pow(az, 2)))))
        yAngle = degrees(atan(ay / (sqrt(pow(ax, 2) + pow(az, 2)))))
        zAngle = degrees(atan(sqrt(pow(ax, 2) + pow(ay, 2)) / az))
        return [xAngle - self.ax, yAngle - self.ay]
