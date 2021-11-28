from setuptools import setup
from os import path

GITHUBLINK = "https://github.com/JoshPattman/spotpuppy"
VERSION = "0.1.8"


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESC = f.read()

setup(name='spotpuppy',
      version=VERSION,
      description='Package for controlling a dynamically balanced quadruped',
      long_description_content_type='text/markdown',
      long_description=LONG_DESC,
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
          "scipy",
      ],
      classifiers=[
        'Development Status :: 3 - Alpha',
      ],
      download_url= GITHUBLINK + "/archive/refs/tags/"+VERSION+".tar.gz",
      )
