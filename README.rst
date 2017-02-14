Opti_SSR
========

This python package provides the necessary tools to use the 
Optitrack optical tracking system for different applications of the SoundScape Renderer (SSR)
including listener position and orientation tracking in local sound field synthesis.

It contains demo functions and several modules that include the functional part.
There is a module to connect to the OptiTrack system (opti_client) and
a seperate one to connect to and control instances of the SSR (ssr_client).
The module that connects these aforementioned ones and implements sequence and desired functionality is also part of the package (bridges).

Note that the optirx 1.10 library is included here with only minor changes from the original source and
that the modules ssr_client and opti_client respectively are designed
to be used independently in other projects as well.

Documentation:
    http://opti-ssr.rtfd.io/

Source code:
    https://github.com/bertmcmeyer/opti_ssr

Python Package Index:
    http://pypi.python.org/pypi/opti_ssr/

License:
    MIT -- see the file ``LICENSE`` for details.

Installation
------------

Aside from Python_ itself, NumPy_ and pyquaternion_ are needed. It should work with both Python3 as well as Python2.

.. _Python: http://www.python.org/
.. _NumPy: http://www.numpy.org/
.. _pyquaternion: http://kieranwynn.github.io/pyquaternion/

The easiest way to install this package is using pip_ to download it from PyPi_::

   pip install opti_ssr

.. _pip: https://pip.pypa.io/en/stable/installing/
.. _PyPi: http://pypi.python.org/pypi/opti_ssr/