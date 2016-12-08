"""
A python module for listener tracking inside the SoundScape Renderer using
the OptiTrack optical tracking system.
"""

from __future__ import print_function
import sys
import threading
import socket
from time import sleep
import numpy as np
from abc import ABCMeta, abstractmethod # for abstract classes and methods

from .opti_client import Quaternion

class _Bridge(threading.Thread):
    """An abstract class which receives data from the optitrack system and
       sends data to the ssr
    """

    # Python2 compatible way to declare an abstract class
    __metaclass__ = ABCMeta

    def __init__(
            self, optitrack, ssr, data_limit=500, timeout=0.01, *args,
            **kwargs):

        # call contructor of super class (threading.Thread)
        super(_Bridge, self).__init__(*args, **kwargs)

        # event triggered to stop execution
        self._quit = threading.Event()

        # interfaces
        self._optitrack = optitrack
        self._ssr = ssr

        # storing older data
        self._data = []  # the data buffer itself
        self._data_limit = data_limit  # maximum number of entries
        self._data_lock = threading.Lock()  # mutex to block access
        self._data_available = threading.Event()  # event for new data

        # timeout
        self._timeout = timeout  # timeout in seconds

    def get_last_data(self, num=None):
        """Returns a list of data received from the OptiTrack system."""
        if not num:
            num = self._data_limit
        return self._data[-num:]

    def clear_data(self):
        """Clears buffer"""
        if self._packet_available.is_set():
            with self._data_lock:  # lock the mutex
                self._packet_data = []
                self._packet_available.clear()

    def run(self):
        while not self._quit.is_set():
            try:
                packet = self._receive()
            except socket.error:  # thrown if not packet has arrived
                sleep(0.1)
            except (KeyboardInterrupt, SystemExit):
                self._quit.set()
            else:
                # save data
                with self._data_lock:
                    self._data.append(packet)
                    self._data = self._data[-self._data_limit:]
                self._data_available.set()
                # send data
                self._send(packet)

    def stop(self):
        self._quit.set()  # fire event to stop execution

    @abstractmethod
    def _receive(self):
        return

    @abstractmethod
    def _send(self, packet):
        return

class HeadTracker(_Bridge):
    """A class for using the OptiTrack system as a head tracker for the SSR
    """

    def __init__(self, optitrack, ssr, rb_id=0, *args, **kwargs):
        # call contructor of super class (_Bridge)
        super(HeadTracker, self).__init__(optitrack, ssr, *args, **kwargs)
        # selects which rigid body from OptiTrack is the head tracker
        self._rb_id = rb_id
        # origin and orientation of world coordinate system
        self._origin = np.array((0, 0, 0))
        self._orientation = Quaternion(1, 0, 0, 0)

    def calibrate(self):
        """
        Use current position and orientation of head tracker to set the origin
        and orientation of the world coordinate system

        Returns
        -------

        """
        self._origin, self._orientation,_ = self._optitrack.get_rigid_body(self._rb_id)

    def _receive(self):
        pos, ori, time_data = self._optitrack.get_rigid_body(self._rb_id)
        # apply coordinate transform
        pos = pos - self._origin
        ori = self._orientation.conjugate * ori  # not commutative

        return pos, ori.yaw_pitch_roll, time_data

    def _send(self, data):
        _, ypr, _ = data  # (pos, ypr, time_data)
        self._ssr.set_ref_orientation(ypr[2]*180/np.pi+90)

class LocalWFS(_Bridge):
    """
    #A class for using the OptiTrack system to track the listener position
    in the SSR for local sound field synthesis.

    The first SSR instance shifts a circular point source array
    placed around the listener in relation to the real reproduction setup.

    The second SSR instance shifts the reference position of aforementioned point sources
    as the virtual reproduction setup in relation to the real sources based on audio files.
    """
    def __init__(self, optitrack, ssr, ssr2, N=64, R=1.00, rb_id=0, *args, **kwargs):
        # call contructor of super class
        super(LocalWFS, self).__init__(optitrack, ssr, *args, **kwargs)
        # selects which rigid body from OptiTrack is the tracker
        self._rb_id = rb_id
        self._N = N
        self._R = R

        # second ssr instance
        self._ssr2 = ssr2

        self._create_virtual_sources()

    def _create_virtual_sources(self):
        """
        Creating a specified amount of new sources via network connection to the SSR.
        """
        for src_id in range(1, self._N+1):
            self._ssr.src_creation(src_id)

    def _receive(self):
        # get position data of rigid body from OptiTrack system
        center, _, _ = self._optitrack.get_rigid_body()

        return center

    def _send(self, center):
        # calculation of source positions in a circular array
        alpha = np.linspace(0, 2 * np.pi, self._N, endpoint=False)
        src_pos = np.zeros((self._N, len(center)))
        src_pos[:, 0] = self._R * np.cos(alpha)
        src_pos[:, 1] = self._R * np.sin(alpha)
        src_pos += center
        # sending position data to SSR; number of source id depends on number of existing sources
        for src_id in range(1, self._N+1):
            self._ssr.set_src_position(src_id, src_pos[src_id-1, 0], src_pos[src_id-1, 1])
            self._ssr2.set_ref_position(center[0], center[1])
