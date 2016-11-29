"""
A python module for listener tracking in local sound field synthesis.
By default, a circular array of virtual point sources is placed around the listener.

Usage: python opti_ssr.py [SSR_IP] [SSR_port] [number of src] [array radius] [optitrack ip] [multicast address] [optitrack port] [end_message]
"""

from __future__ import print_function
import sys
import numpy as np

from opti_network import opti_network
from ssr_network import ssr_network

# server IP, running the SSR
# Mac IP/wall-e: 139.30.207.123
# Debian IP: 139.30.207.218

class ssr_localwfs:
    """
    #TODO
    """
    def __init__(self, ssr_ip='139.30.207.123', ssr_port=4711, N=64, R=1.00, opti_ip=None, multicast_address='239.255.42.99', opti_port=1511, end_message='\0'):
        self._N = N
        self._R = R

        # evtl nicht noetig?
        self._ssr_ip = ssr_ip
        self._ssr_port = ssr_port
        self._opti_ip = opti_ip
        self._multicast_address = multicast_address
        self._opti_port = opti_port

        self._end_message = end_message
        self._ssr = ssr_network(self._ssr_ip, self._ssr_port, self._end_message)
        self._optitrack = opti_network(self._opti_ip, self._multicast_address, self._opti_port)

    def create_src(self):
        """
        Creating a specified amount of new sources via network connection to the SSR.
        """
        for src_id in range(1, self._N+1):
            self._ssr.src_creation(src_id)

    def src_pos_circular_array(self):
        """
        Defining source positions in a circular array based on the received data.
        """
        # get position data from Motive
        x, y, z = self._optitrack.get_rigid_body_position()[0]
        # z-coordinate of Motive is the y-coordinate of the SSR
        # evtl. -x
        center = [x, z, 0]

        # calculation of source positions in a circular array
        alpha = np.linspace(0, 2 * np.pi, self._N, endpoint=False)
        src_pos = np.zeros((self._N, len(center)))
        src_pos[:, 0] = self._R * np.cos(alpha)
        src_pos[:, 1] = self._R * np.sin(alpha)
        src_pos += center

        # sending position data to SSR; number of source id depends on number of existing sources
        for src_id in range(1, self._N+1):
            self._ssr.set_src_position(src_id, src_pos[src_id-1, 0], src_pos[src_id-1, 1])


def ssr_send(ssr_ip='139.30.207.123', ssr_port=4711, N=64, R=1.00, opti_ip=None, multicast_address='239.255.42.99', opti_port=1511, end_message='\0'):
    """ #todo

    Parameters
    ----------
    IP : str, optional
        IP of the server running thr SSR.
    port : int, optional
        Port of SSR Network Interface. By default, port = 4711.
    buffer : int, optional
        Buffersize. By default, buffersize = 1024.
    N : int, optional
        Number of Sources. By default, 12 sources.
    R : float, optional
        Radius of circular source array in meter. By default, 1m.
    end_message : str, optional
        Symbol to terminate the XML messages send to SSR. By default, a binary zero.

    """
    # setting arguments if executed in command line
    if sys.argv[1:]:
        ssr_ip = str(sys.argv[1])
    if sys.argv[2:]:
        ssr_port = int(sys.argv[2])
    if sys.argv[3:]:
        N = int(sys.argv[3])
    if sys.argv[4:]:
        R = float(sys.argv[4])
    if sys.argv[5:]:
        opti_ip = str(sys.argv[5])
    if sys.argv[6:]:
        multicast_address = str(sys.argv[6])
    if sys.argv[7:]:
        opti_port = str(sys.argv[7])
    if sys.argv[8:]:
        end_message = str(sys.argv[8])


    opti_ssr = ssr_localwfs(ssr_ip, ssr_port, N, R, end_message)
    opti_ssr.create_src()
    while True:
        opti_ssr.src_pos_circular_array()
    del opti_ssr



if __name__ == "__main__":
    ssr_send()