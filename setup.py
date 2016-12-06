import os
from setuptools import setup

setup(
    name = "opti_ssr",
    version = "0.0.4",
    py_modules=['opti_ssr', 'ssr_network', 'opti_network'],
    author = "Felix Immohr, Fiete Winter",
    author_email = "test@te.st, fiete.winter@gmail.com",
    description = ("Using the OptiTrack system for different applications "
                    "of the SoundScape Renderer"),
    license = "MIT",
    keywords = "optitrack motive natnet ssr soundscaperenderer".split(),
    url = "",
    long_description=open('README').read(),
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
