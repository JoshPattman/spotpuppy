from . import dummy_rotation_sensor
try:
    from . import mpu6050_rotation_sensor
except:
    print("Can't import mpu6050_rotation_sensor (rpi only) (try installing mpu6050)")