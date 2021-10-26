# Spot Puppy Python Library
Have a look at the [github](https://github.com/JoshPattman/spotpuppy) for more info
## What this package is for
This package is a framework for controlling dynamically balanced 4 legged robots. It's purpose is to abstract the low-level maths and functionality away from the user, and provide useful helper functionality to make designing a walking algorithm an easy job. The package splits up the walking algorithm implementation and usage, which means that it is simple to write multiple programs using the same algorithm, without having to copy code.
## This is a development package
This package is still in alpha development so is probably full of bugs. If you find any, please feel free to raise a github issue or fix it and create a pull request!
## Installation
This package is on pip so you can use `pip install spotpuppy`
> There are a few built in types in this package that require specific package or modules to run (e.g. `mpu6050_rotation_sensor.sensor` requires the `mpu6050` package for rpi). These only have to be installed when you want to use the modules, but can be ignored if you are not using them. If a required module is not found, an `ImportError` will be thrown
## Usage
Check out the [wiki](https://github.com/JoshPattman/spotpuppy/wiki) for information on usage of the library
