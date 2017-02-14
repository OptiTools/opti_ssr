Opti_SSR
========

This python package provides the necessary tools to use the 
Optitrack optical tracking system for different applications of the SoundScape Renderer (SSR)
including listener position and orientation tracking in local sound field synthesis.

It contains several modules including a module to connect to the OptiTrack system (opti_client) and
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

The easiest way to install this package is using pip_ to download the latest release from PyPi_::

   pip install opti_ssr

.. _pip: https://pip.pypa.io/en/stable/installing/
.. _PyPi: http://pypi.python.org/pypi/opti_ssr/

Usage
-----
To use opti_ssr you can use a demo function like the basic one below.
Simply instatiate the necessary class objects according to the given parameters and start the thread in the class that contains the functionality.
Ready-to-use demo functions to demonstrate head orientation tracking in binaural synthesis or 
listener tracking in local sound field synthesis are available at the github repository. ::

    import opti_ssr

    def demo(ssr_ip, ssr_port, opti_unicast_ip, opti_multicast_ip, opti_port, ssr_end_message):
        optitrack = opti_ssr.OptiTrackClient(opti_unicast_ip, opti_multicast_ip, opti_port)
        ssr = opti_ssr.SSRClient(ssr_ip, ssr_port, ssr_end_message)
        headtracker = opti_ssr.HeadTracker(optitrack, ssr)
        headtracker.start()

    if __name__ == "__main__":
        demo()