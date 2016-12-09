"""
A python module to connect to Optitrack system
and receiving data, including rigid-body position and orientation, from it.
By default, it connects to Optitrack software Motive on the same machine.
"""

from . import optirx as rx
import numpy as np
import pyquaternion  # for handling quaternions

class OptiTrackClient:
    """
    #TODO
    """

    def __init__(self, unicast_ip=None, multicast_ip="239.255.42.99", port=1511, natnet_version=(3, 0, 0, 0)):
        self._dsock = rx.mkdatasock(ip_address=unicast_ip, multicast_address=multicast_ip, port=port)
        self._natnet_version = natnet_version

    def get_packet_data(self, packet_types=[rx.SenderData, rx.ModelDefs, rx.FrameOfData]):
        """
        Connect to Optitrack system (by default, on the same machine)
        and receiving packet data from it.

        based on optirx-demo.py
        source: https://bitbucket.org/astanin/python-optirx

        Parameters
        ----------
        packet_types : list, optional
            types of the packets to be returned

        Returns
        -------


        """
        while True:
            data = self._dsock.recv(rx.MAX_PACKETSIZE)
            packet = rx.unpack(data, version=self._natnet_version)
            if not packet_types or type(packet) in packet_types:
                return packet

    def get_rigid_body(self, rb_id=0):
        """
        Connect to Optitrack system and receiving rigid body data from it.

        Parameters
        ----------
        rb_id : int, optional
            ID of the rigid body to receive data from.

        Returns
        -------


        """
        packet = self.get_packet_data()

        position = np.array(packet.rigid_bodies[rb_id].position)
        orientation = Quaternion(packet.rigid_bodies[rb_id].orientation)
        time_data = (packet.timestamp, packet.timecode, packet.latency)

        return position, orientation, time_data

class Quaternion(pyquaternion.Quaternion):
    """Work-around until pull request for original packages is accepted
    https://github.com/KieranWynn/pyquaternion/pull/2
    """

    @property
    def yaw_pitch_roll(self):
        """
        Get the equivalent yaw-pitch-roll angles aka. intrinsic Tait-Bryan
        angles following the z-y'-x'' convention

        Returns
        -------
        yaw: double
            rotation angle around the z-axis in radians, in the range
            `[-pi, pi]`
        pitch: double
            rotation angle around the y'-axis in radians, in the range
            `[-pi/2, -pi/2]`
        roll: double
            rotation angle around the x''-axis in radians, in the range
            `[-pi, pi]`

        Note
        ----
        This feature only makes sense when referring to a unit quaternion.
        Calling this method will implicitly normalise the Quaternion object
        to a unit quaternion if it is not already one.
        """

        self._normalise()
        yaw = np.arctan2(2*(self.q[0]*self.q[3] + self.q[1]*self.q[2]),
            1 - 2*(self.q[2]**2 + self.q[3]**2))
        pitch = np.arcsin(2*(self.q[0]*self.q[2] - self.q[3]*self.q[1]))
        roll = np.arctan2(2*(self.q[0]*self.q[1] + self.q[2]*self.q[3]),
            1 - 2*(self.q[1]**2 + self.q[2]**2))

        return yaw, pitch, roll

