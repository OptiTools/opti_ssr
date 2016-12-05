"""
#todo
"""

from __future__ import print_function
import sys
import threading
import socket
from time import sleep
from numpy import pi
from abc import ABCMeta, abstractmethod # for abstract classes and methods

from opti_network import opti_network
from ssr_network import ssr_network

class _Bridge(threading.Thread):
    """An abstract class which receives some data from optitrack and sends some
       other data to the ssr
    """
    
    __metaclass__ = ABCMeta

    def __init__(self, optitrack, ssr, data_limit=500, timeout=0.01, *args,
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
        self._data_lock = threading.Lock()  #  mutex to block access
        self._data_available = threading.Event()  # event for new data
        
        # timeout
        self._timeout = timeout  # timeout in seconds

    def get_last_data(self):
        """Returns a list of data received from the OptiTrack system."""
        return self._data
       
    def clear_data(self):
        """Clears buffer"""
        if self._packet_available.is_set():
            with self._data_lock:  # lock the mutex
                self._packet_data = []
                self._packet_available.clear()

    def run(self):
        while not self._quit.is_set():
            try:
                # get the data    
                packet = self._receive()  # dummy data
            except socket.error: 
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
        # call contructor of super class
        super(HeadTracker, self).__init__(optitrack, ssr, *args, **kwargs)
        
        # selects which rigid body from OptiTrack is the head tracker
        self._rb_id = rb_id
        self._optitrack = optitrack 
        self._ssr = ssr
        
    def _receive(self):
        rigid_body = self._optitrack.get_rigid_body(self._rb_id)
        # positions
        pos = rigid_body.position
        # yaw pitch roll angles
        q = _Quaternion(rigid_body.orientation)
        ypr = q.yaw_pitch_roll
        #
        return pos, ypr 
    
    def _send(self, rigid_body):
        _, ypr = rigid_body
        self._ssr.ref_orientation(angle*180/pi)

