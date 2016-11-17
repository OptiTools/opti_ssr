"""
#todo
"""

from __future__ import print_function
import sys
import socket
import optirx as rx
import numpy as np


# server IP, running the SSR
# Mac IP/wall-e: 139.30.207.123
# Debian IP: 139.30.207.218 ++

def recv_data():
    """
    connect to Optitrack system on the same machine and receiving data from it

    based on optirx-demo.py
    source: https://bitbucket.org/astanin/python-optirx
    """

    dsock = rx.mkdatasock()
    while True:
        data = dsock.recv(rx.MAX_PACKETSIZE)
        packet = rx.unpack(data, version=version)
        if type(packet) is rx.SenderData:
            version = packet.natnet_version
            print("NatNet version received:", version)
        if type(packet) in [rx.SenderData, rx.ModelDefs, rx.FrameOfData]:
		    # z-coordinate of Motive is the y-coordinate of the SSR
            x = packet.rigid_bodies[0].position[0]
            y = packet.rigid_bodies[0].position[1]
            z = packet.rigid_bodies[0].position[2]
            return x, y, z

def src_creation(N, end_message):
    """
    generating the XML message to create new sources in the SSR

    Parameters
    ----------
    N : int, optional
        Number of Sources.
    end_message : str, optional
        Symbol to terminate the XML messages send to SSR.

    Returns
    -------

    """
    new_sources = '<request>'
    for i in range(1, N+1):
        source = '<source new="true" id="{0}" port="0"></source>'.format(i)
        new_sources += source
    new_sources = new_sources+'</request>'+end_message
    return new_sources

def src_position(N, R, end_message):
    """
    defining source positions based on the received data

    Parameters
    ----------
    N : int, optional
        Number of Sources.
    R : int, optional
        Radius of circular source array in meter.
    end_message : str, optional
        Symbol to terminate the XML messages send to SSR.

    Returns
    -------


    """
    # z-coordinate of Motive is the y-coordinate of the SSR
    x, y, z = recv_data()
    center = [x, z, 0]

    # definition of source positions in a circular array
    alpha = np.linspace(0, 2 * np.pi, N, endpoint=False)
    positions = np.zeros((N, len(center)))
    positions[:, 0] = R * np.cos(alpha)
    positions[:, 1] = R * np.sin(alpha)
    positions += center

    # number of the source id depends on the number of existing sources
    src_pos = '<request>'
    for i in range(1, N+1):
        src_pos += '<source id="{0}" name="SourceMotive{0}"><position x="{1:4.2f}" y="{2:4.2f}"/></source>'.format(i, positions[i-1, 0], positions[i-1, 1])
    src_pos += '</request>'+ end_message
    return src_pos

def ssr_send(IP='139.30.207.123', port=4711, buffer=1024, N=12, R=1, end_message='\0'):
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
        buffer = int(sys.argv[3])
    if sys.argv[4:]:
        N = int(sys.argv[4])
    if sys.argv[5:]:
        R = float(sys.argv[5])
    if sys.argv[6:]:
        end_message = str(sys.argv[6])

    # IP4 und TCP connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connection to the server
    s.connect((IP, port))

    # creating a new source, which gets the coordinates from Motive
    new_sources = src_creation(N, end_message)

    # sending the source and position data to SSR
    s.send(new_sources.encode())
    while True:
        position = src_position(N, R, end_message)
        s.send(position.encode())

    s.close()



if __name__ == "__main__":
    ssr_send()
