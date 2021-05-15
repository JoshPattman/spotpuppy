from distutils.core import setup

setup(name='spotpuppy',
      version='0.0.1',
      description='Package for controlling a dynamically balanced quadruped',
      long_description=['This package contains code to easily get a quadruped up and running. It also contains extendable classes to allow you to write your own balancing algorithms and gaits'],
      author='Josh Pattman',
      author_email='josh.pattman@gmail.com',
      packages=['spotpuppy',
                'spotpuppy.core',
                'spotpuppy.models',
                'spotpuppy.rotation',
                'spotpuppy.servo',
                'spotpuppy.utils'],
      install_requires=[
          "numpy",
      ],
      )
