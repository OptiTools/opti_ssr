import os
from setuptools import setup

setup(
    name = "opti_ssr",
    version = "0.0.4",
    packages=['opti_ssr'],
    author = "Felix Immohr, Fiete Winter, Sergey Astanin",
    author_email = "fiete.winter@gmail.com",
    description = ("Using the OptiTrack system for different applications "
                    "of the SoundScape Renderer"),
    license = "MIT",
    keywords = "optitrack motive natnet ssr soundscaperenderer".split(),
    url = "",
    long_description=open('README.rst').read(),
    platforms='any',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
