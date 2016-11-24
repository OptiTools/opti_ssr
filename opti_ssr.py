"""
#todo
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
    #todo
    """
    def __init__(self, IP='139.30.207.218', port=4711, N=64, R=1.00, end_message='/0'):
        self._N = N
        self._R = R
        self._ip = IP
        self._port = port

        self._end_message = end_message
        self._ssr_net = ssr_network(self._ip, self._port, self._end_message)
        self._opti_net = opti_network()

    def __del__(self):
        del self._ssr_net
        del self._opti_net

    def create_src(self):
        """
        creating a specified amount of new sources via network connection to the SSR
        """
        for src_id in range(1, self._N+1):
            self._ssr_net.src_creation(src_id)

    def src_pos_circular_array(self):
        """
        defining source positions in a circular array based on the received data

        """
        # get position data from Motive
        x, y, z = self._opti_net.get_rigid_body_position()
        # z-coordinate of Motive is the y-coordinate of the SSR
        center = [x, z, 0]

        # calculation of source positions in a circular array
        alpha = np.linspace(0, 2 * np.pi, self._N, endpoint=False)
        src_pos = np.zeros((self._N, len(center)))
        src_pos[:, 0] = self._R * np.cos(alpha)
        src_pos[:, 1] = self._R * np.sin(alpha)
        src_pos += center

        # sending position data to SSR; number of the source id depends on the number of existing sources
        for src_id in range(1, self._N+1):
            self._ssr_net.src_position(src_id, src_pos[src_id-1, 0], src_pos[src_id-1, 1])


def ssr_send(IP='139.30.207.123', port=4711, N=12, R=1.00, end_message='\0'):
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

    Returns
    -------

    """
    # setting arguments if executed in command line
    if sys.argv[1:]:
        IP = str(sys.argv[1])
    if sys.argv[2:]:
        port = int(sys.argv[2])
    if sys.argv[3:]:
        N = int(sys.argv[3])
    if sys.argv[4:]:
        R = float(sys.argv[4])
    if sys.argv[5:]:
        end_message = str(sys.argv[5])


    opti_ssr = ssr_localwfs(IP, port, N, R, end_message)
    opti_ssr.create_src()
    while True:
        opti_ssr.src_pos_circular_array()
    del opti_ssr



if __name__ == "__main__":
    ssr_send()
