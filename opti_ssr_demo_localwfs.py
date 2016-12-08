"""
A python module for demonstrating listener tracking in local sound field synthesis.
By default, a circular array of virtual point sources is placed around the listener.

Usage: python opti_ssr_demo.py [SSR_IP] [SSR_port] [number of src] [array radius] [optitrack ip] [multicast address] [optitrack port] [ssr end message]
"""

import sys
import opti_ssr

def demo(ssr_ip='localhost', ssr_port=4711, N=64, R=1.00, opti_unicast_ip=None, opti_multicast_ip='239.255.42.99', opti_port=1511, ssr_end_message='\0'):
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
    ssr_end_message : str, optional
        Symbol to terminate the XML messages send to SSR. By default, a binary zero.

    """
    # setting arguments if executed in command line
    if sys.argv[1:]:
        ssr_ip = str(sys.argv[1])
    if sys.argv[2:]:
        ssr_port = int(sys.argv[2])
    if sys.argv[3:]:
        ssr2_port = int(sys.argv[3])
    if sys.argv[4:]:
        N = int(sys.argv[4])
    if sys.argv[5:]:
        R = float(sys.argv[5])
    if sys.argv[6:]:
        opti_unicast_ip = str(sys.argv[6])
    if sys.argv[7:]:
        opti_multicast_ip = str(sys.argv[7])
    if sys.argv[8:]:
        opti_port = str(sys.argv[8])
    if sys.argv[9:]:
        ssr_end_message = str(sys.argv[9])

    # instantiation of the necessary class objects
    optitrack = opti_ssr.OptiTrackClient(opti_unicast_ip, opti_multicast_ip, opti_port)
    ssr = opti_ssr.SSRClient(ssr_ip, ssr_port, ssr_end_message)
    ssr2 = opti_ssr.SSRClient(ssr_ip, ssr2_port, ssr_end_message)
    localwfs = opti_ssr.LocalWFS(optitrack, ssr, ssr2, N, R)

    # creating sources once and continuously tracking position
    localwfs.start()

if __name__ == "__main__":
    demo()
