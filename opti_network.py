"""
A python module to connect to Optitrack system on the same machine and receiving rigid-body position and orientation data from it
"""

import optirx as rx
import numpy as np
import pyquaternion  # for handling quaternions

class opti_network:
    """
    #todo
    """ 
    def __init__(self, SDK_version=(3, 0, 0, 0)):
        self._dsock = rx.mkdatasock()
        self._SDK_version = SDK_version

    def get_packet(self, packet_types=None):
        while True:
            data = self._dsock.recv(rx.MAX_PACKETSIZE)
            packet = rx.unpack(data, version=self._SDK_version)
            if not packet_types or type(packet) in packet_types:
                return packet
            
    def get_rigid_body(self, rb_id):
        
        packet = self.get_packet([rx.SenderData, rx.ModelDefs, rx.FrameOfData])g
        return packet.rigid_bodies[rb_id]

    def get_rigid_body_position(self, rb_id):

        rigid_body = self.get_rigid_body(rb_id)
        return rigid_body.position

    def get_rigid_body_orientation(self, rb_id, yaw_pitch_roll=False):
        
        rigid_body = self.get_rigid_body(rb_id)
        if yaw_pitch_roll:
            q = _Quaternion(rigid_body.orientation)
            return q.yaw_pitch_roll
        else:
            return rigid_body.orientation       

class _Quaternion(pyquaternion.Quaternion):
    """Work-around until pull request for original packages is accepted
    https://github.com/KieranWynn/pyquaternion/pull/2
    """

    @property
    def yaw_pitch_roll(self):
        """Get the equivalent yaw-pitch-roll angles aka. intrinsic Tait-Bryan angles following the z-y'-x'' convention
        
        Returns:
            yaw:    rotation angle around the z-axis in radians, in the range `[-pi, pi]`
            pitch:  rotation angle around the y'-axis in radians, in the range `[-pi/2, -pi/2]`
            roll:   rotation angle around the x''-axis in radians, in the range `[-pi, pi]` 
        
        The resulting rotation_matrix would be R = R_x(roll) R_y(pitch) R_z(yaw)
            
        Note: 
            This feature only makes sense when referring to a unit quaternion. Calling this method will implicitly normalise the Quaternion object to a unit quaternion if it is not already one.
        """
        
        self._normalise()
        yaw = np.arctan2(2*(self.q[0]*self.q[3] - self.q[1]*self.q[2]), 
            1 - 2*(self.q[2]**2 + self.q[3]**2))
        pitch = np.arcsin(2*(self.q[0]*self.q[2] + self.q[3]*self.q[1]))
        roll = np.arctan2(2*(self.q[0]*self.q[1] - self.q[2]*self.q[3]), 
            1 - 2*(self.q[1]**2 + self.q[2]**2))

        return yaw, pitch, roll

