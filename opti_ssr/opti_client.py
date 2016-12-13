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
    A class to connect to Optitrack systems and Motive software and receive data from it.

    Attributes
    ----------
    unicast_ip : str, optional
        IP of the Motive software to establish a unicast connection to.
        By default, no unicast connection is established.
    multicast_ip : str, optional
        Multicast address to connect to.
    port : int, optional
        Port of the Motive network interface.
    natnet_version : tuple, optional
        Version number of the NatNetSDK to use.
    """

    def __init__(self, unicast_ip=None, multicast_ip="239.255.42.99", port=1511, natnet_version=(3, 0, 0, 0)):
        self._dsock = rx.mkdatasock(ip_address=unicast_ip, multicast_address=multicast_ip, port=port)
        self._natnet_version = natnet_version

    def get_packet_data(self, packet_types=[rx.SenderData, rx.ModelDefs, rx.FrameOfData]):
        """
        Connect to Optitrack system (by default, on the same machine)
        and receive packet data from it.

        based on optirx-demo.py
        source: https://bitbucket.org/astanin/python-optirx

        Parameters
        ----------
        packet_types : list, optional
            Types of the packets to be returned.

        Returns
        -------
        packet : list
            Received packets of desired type.

        """
        while True:
            data = self._dsock.recv(rx.MAX_PACKETSIZE)
            packet = rx.unpack(data, version=self._natnet_version)
            if not packet_types or type(packet) in packet_types:
                return packet

    def get_rigid_body(self, rb_id=0):
        """
        Connect to Optitrack system and receive complete rigid body data from it.

        Parameters
        ----------
        rb_id : int, optional
            ID of the rigid body to receive data from.

        Returns
        -------
        rigid_body : list
            Complete rigid body packet data of the desired rigid body.
        time_data : list
            List of time data consisting of timestamp, timecode and latency packet data.

        """
        packet = self.get_packet_data()
        rigid_body = packet.rigid_bodies[rb_id]
        time_data = (packet.timestamp, packet.timecode, packet.latency)
        return rigid_body, time_data


    def get_rigid_body_position(self, rb_id=0):
        """
        Connect to Optitrack system and receive rigid body position and time data from it.

        Parameters
        ----------
        rb_id : int, optional
            ID of the rigid body to receive data from.

        Returns
        -------
        x : int
            X coordinate of the desired rigid body in Motive`s coordinate system.
        y : int
            Y coordinate of the desired rigid body in Motive`s coordinate system.
        z : int
            Z coordinate of the desired rigid body in Motive`s coordinate system.
        time_data : list
            List of time data consisting of timestamp, timecode and latency packet data.

        """
        rigid_body, time_data = self.get_rigid_body(rb_id)
        return rigid_body.position, time_data

    def get_rigid_body_orientation(self, rb_id=0):
        """
        Connect to Optitrack system and receive rigid body orientation and time data from it.
        The quarternion output of the Motive software is converted into intrinsic Tait-Bryan angles.

        Parameters
        ----------
        rb_id : int, optional
            ID of the rigid body to receive data from.

        Returns
        -------
        yaw : double
            
            Rotation angle around the z-axis in radians, in the range
            `[-pi, pi]`
        pitch : double
            Rotation angle around the y'-axis in radians, in the range
            `[-pi/2, -pi/2]`
        roll : double
            Rotation angle around the x''-axis in radians, in the range
            `[-pi, pi]`
        time_data : list
            List of time data consisting of timestamp, timecode and latency packet data.

        """
        rigid_body, time_data = self.get_rigid_body(rb_id)
        # Motive quaternion orientation
        q = Quaternion(rigid_body.orientation)
        # Convert Motive quaternion output to euler angles and return it in addition to time data
        return q.yaw_pitch_roll, time_data

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

