import json
import numpy as np
import os


def vec_2_to_json(vec, labels=["X", "Z"]):
    return {labels[0]: float(vec[0]), labels[1]: float(vec[1])}


def vec_3_to_json(vec, labels=["X", "Y", "Z"]):
    return {labels[0]: float(vec[0]), labels[1]: float(vec[1]), labels[2]: float(vec[2])}


def json_to_vec_2(js, labels=["X", "Z"]):
    return np.array([float(js[labels[0]]), float(js[labels[1]])])


def json_to_vec_3(js, labels=["X", "Y", "Z"]):
    return np.array([float(js[labels[0]]), float(js[labels[1]]), float(js[labels[2]])])


def save_json_dict(filename, dict):
    if dict == None:
        return
    s = json.dumps(dict, indent=4)
    with open(filename, 'w') as f:
        f.write(s)


def load_json_dict(filename):
    if not os.path.exists(filename):
        print("Could not find " + filename + ", ignoring")
        return
    with open(filename, 'r') as f:
        return json.loads(f.read())


def save_robot(quad, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print("Folder did not exist, creating one...")
    robot_config = quad.get_json_dict()
    servo_map = quad.servo_controller.get_json()
    leg_cal = {}
    leg_names = ["FL", "FR", "BL", "BR"]
    for l in range(4):
        leg_cal[leg_names[l]] = quad.quad_controller.legs[l].to_json_dict()
    accel_cal = quad.rotation_sensor.get_json_params()
    save_json_dict(folder_name + "/robot_config.json", robot_config)
    save_json_dict(folder_name + "/servo_map.json", servo_map)
    save_json_dict(folder_name + "/leg_setup.json", leg_cal)
    save_json_dict(folder_name + "/gyro.json", accel_cal)


def load_into_robot(quad, folder_name):
    if not os.path.exists(folder_name):
        print("Specified config directory does not exist")
        return
    robot_config = load_json_dict(folder_name + "/robot_config.json")
    servo_map = load_json_dict(folder_name + "/servo_map.json")
    leg_cal = load_json_dict(folder_name + "/leg_setup.json")
    accel_cal = load_json_dict(folder_name + "/gyro.json")

    quad.rotation_sensor.set_json_params(accel_cal)
    quad.set_json_dict(robot_config)
    quad.servo_controller.set_json(servo_map)
    leg_names = ["FL", "FR", "BL", "BR"]
    for l in range(4):
        quad.quad_controller.legs[l].load_json_dict(leg_cal[leg_names[l]])
