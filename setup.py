from distutils.core import setup

def readme():
    with open("README.md", 'r') as f:
        return f.read()

VERSION = "0.0.2"

setup(name='spotpuppy',
      version=VERSION,
      description='Package for controlling a dynamically balanced quadruped',
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
