from distutils.core import setup
from os import path

def readme():
    return "This package contains code to easily get a quadruped up and running. It also contains extendable classes to allow you to write your own balancing algorithms and gaits"
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()

VERSION = "0.0.6"

setup(name='spotpuppy',
      version=VERSION,
      description='Package for controlling a dynamically balanced quadruped',
      long_description_content_type='text/markdown',
      long_description=readme(),
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
      classifiers=[
        'Development Status :: 3 - Alpha',
      ],
      download_url="https://github.com/JoshPattman/Spot-Puppy-Lib/archive/refs/tags/"+VERSION+".tar.gz",
      )
