"""
A python module to connect to Optitrack system on the same machine and receiving rigid-body position and orientation data from it
"""

import optirx as rx
import numpy as np

class opti_network:
    """
    #todo
    """ 
    def __init__(self, SDK_version=(3, 0, 0, 0), rb_id=0):
        self._rb_id = rb_id
        self._dsock = rx.mkdatasock()
        self._SDK_version = SDK_version

    def get_rigid_body_position(self):
        """
        connect to Optitrack system on the same machine and receiving data from it

        based on optirx-demo.py
        source: https://bitbucket.org/astanin/python-optirx
        """

        while True:
            data = self._dsock.recv(rx.MAX_PACKETSIZE)
            packet = rx.unpack(data, version=self._SDK_version)
            if type(packet) is rx.SenderData:
                version = packet.natnet_version
                print("NatNet version received:", version)
            if type(packet) in [rx.SenderData, rx.ModelDefs, rx.FrameOfData]:
		        # z-coordinate of Motive is the y-coordinate of the SSR
                x = packet.rigid_bodies[self._rb_id].position[0]
                y = packet.rigid_bodies[self._rb_id].position[1]
                z = packet.rigid_bodies[self._rb_id].position[2]
                return x, y, z

    def get_rigid_body_orientation(self):
        # roll, pitch, yaw zurueckgeben
        # mit .orientation[0-3]
        # Quaternionen --> "Gimbel-Lock"-problem
        # Quaternionen --> Rotationsmatrix bestimmen?
        # Bsp. zur umwandlung der Quarternionen in C in NatNetSDK ... irgendwas mit simple...3D.cpp
        while True:
            data = self._dsock.recv(rx.MAX_PACKETSIZE)
            packet = rx.unpack(data, version=self._SDK_version)
            if type(packet) is rx.SenderData:
                version = packet.natnet_version
                print("NatNet version received:", version)
            if type(packet) in [rx.SenderData, rx.ModelDefs, rx.FrameOfData]:
                # Motive quaternion orientation data output
                qx = packet.rigid_bodies[self._rb_id].orientation[0]
                qy = packet.rigid_bodies[self._rb_id].orientation[1]
                qz = packet.rigid_bodies[self._rb_id].orientation[2]
                qw = packet.rigid_bodies[self._rb_id].orientation[3]
            # Convert Motive quaternion output to euler angles
            # Motive coordinate conventions : X(Pitch), Y(Yaw), Z(Roll), Relative, RHS

