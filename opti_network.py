"""
A python module to connect to Optitrack system
and receiving data, including rigid-body position and orientation, from it.
By default, it connects to Optitrack software Motive on the same machine.
"""

import optirx as rx
import numpy as np
import pyquaternion  # for handling quaternions

class opti_network:
    """
    #TODO
    """

    def __init__(self, opti_ip=None, multicast_address="239.255.42.99", opti_port=1511, NatNet_version=(3, 0, 0, 0)):
        self._dsock = rx.mkdatasock(ip_address=opti_ip, multicast_address=multicast_address, port=opti_port)
        self._NatNet_version = NatNet_version

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
            packet = rx.unpack(data, version=self._NatNet_version)
            if type(packet) is rx.SenderData:
                version = packet.natnet_version
                print("NatNet version received:", version)
            if type(packet) in packet_types:
                return packet


    def get_rigid_body_position(self, rb_id=0):
        """
        Connect to Optitrack system and receiving rigid body position data from it.

        Parameters
        ----------
        rb_id : int, optional
            ID of the rigid body to receive data from.

        Returns
        -------


        """
        packet = self.get_packet_data()
        position = packet.rigid_bodies[rb_id].position
        time_data = [packet.timestamp, packet.timecode, packet.latency]
        return position, time_data

    def get_rigid_body_orientation(self, rb_id=0):
        """
        Connect to Optitrack system and receiving rigid body orientation data from it.

        Parameters
        ----------
        rb_id : int, optional
            ID of the rigid body to receive data from.

        Returns
        -------


        """
        packet = self.get_packet_data()
        # Motive quaternion orientation and time data output
        q = _Quaternion(packet.rigid_bodies[rb_id].orientation)
        time_data = [packet.timestamp, packet.timecode, packet.latency]
        # Convert Motive quaternion output to euler angles and return it in addition to time data
        return q.yaw_pitch_roll, time_data


class _Quaternion(pyquaternion.Quaternion):

    @property
    def yaw_pitch_roll(self):
        """Get the equivalent yaw-pitch-roll angles aka. intrinsic Tait-Bryan angles following the z-y'-x'' convention

        Returns:
            yaw:    rotation angle around the z-axis in radians, in the range `[-pi, pi]`
            pitch:  rotation angle around the y'-axis in radians, in the range `[-pi/2, -pi/2]`
            roll:   rotation angle around the x''-axis in radians, in the range `[-pi, pi]` 

        Note: 
            This feature only makes sense when referring to a unit quaternion. Calling this method will implicitly normalise the Quaternion object to a unit quaternion if it is not already one.
        """

        self._normalise()
        yaw = np.arctan2(2*(self.q[0]*self.q[3] + self.q[1]*self.q[2]), 
            1 - 2*(self.q[2]**2 + self.q[3]**2))
        pitch = np.arcsin(2*(self.q[0]*self.q[2] - self.q[3]*self.q[1]))
        roll = np.arctan2(2*(self.q[0]*self.q[1] + self.q[2]*self.q[3]), 
            1 - 2*(self.q[1]**2 + self.q[2]**2))

        return yaw, pitch, roll
