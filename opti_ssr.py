"""
A python module for listener tracking in local sound field synthesis.
By default, a circular array of virtual point sources is placed around the listener.
"""

from __future__ import print_function
import numpy as np

# server IP, running the SSR
# Mac IP/wall-e: 139.30.207.123
# Debian IP: 139.30.207.218

class ssr_localwfs:
    """
    #TODO
    """
    def __init__(self, optitrack, ssr, N=64, R=1.00):
        self._N = N
        self._R = R
        self._ssr = ssr
        self._optitrack = optitrack

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
