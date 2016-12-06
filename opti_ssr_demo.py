"""
A python module for demonstrating listener tracking in local sound field synthesis.
By default, a circular array of virtual point sources is placed around the listener.

Usage: python opti_ssr_demo.py [SSR_IP] [SSR_port] [number of src] [array radius] [optitrack ip] [multicast address] [optitrack port] [end_message]
"""

import sys

from opti_network import opti_network
from ssr_network import ssr_network
from opti_ssr import ssr_localwfs

# server IP, running the SSR
# Mac IP/wall-e: 139.30.207.123
# Debian IP: 139.30.207.218

def opti_ssr_demo(ssr_ip='139.30.207.123', ssr_port=4711, N=64, R=1.00, opti_ip=None, multicast_address='239.255.42.99', opti_port=1511, end_message='\0'):
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

    # instantiation of the necessary class objects
    optitrack = opti_network(opti_ip, multicast_address, opti_port)
    ssr = ssr_network(ssr_ip, ssr_port, end_message)
    opti_ssr = ssr_localwfs(optitrack, ssr, N, R)

    # creating sources once and continuously tracking position
    opti_ssr.create_src()
    while True:
        opti_ssr.src_pos_circular_array()
    del opti_ssr

if __name__ == "__main__":
    opti_ssr_demo()
