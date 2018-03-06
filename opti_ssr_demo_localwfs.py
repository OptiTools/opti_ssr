"""
A python module for demonstrating listener tracking in local wave field synthesis.

To accomplish the listener tracking two instances of the SoundScape Renderer (SSR) are necessary.
The first SSR instance shifts a the reference position of a real reproduction setup in relation
to a virtual point source array placed around the listener at the center.
The second SSR instance shifts the reference position of aforementioned point sources
as the virtual reproduction setup in relation to the real sources based on audio files.

Usage: python opti_ssr_demo.py [SSR_IP] [SSR1 port] [SSR2 port] [number of src] [array radius] [optitrack ip] [multicast address] [optitrack port] [ssr end message]
"""

import sys
import opti_ssr

def demo(ssr_ip='localhost', ssr_port=4711, ssr2_port=4712, opti_unicast_ip=None, opti_multicast_ip='239.255.42.99', opti_port=1511, ssr_end_message='\0'):
    """ A demo function to track the listener position.

    Parameters
    ----------
    ssr_ip : str, optional
        IP of the server running the SSR.
    ssr_port : int, optional
        Port of the first SSR`s Network Interface. By default, port 4711.
    ssr2_port : int, optional
        Port of the second SSR`s Network Interface. By default, port 4712.
    opti_unicast_ip : str, optional
        IP of the Motive software to establish a unicast connection to.
        By default, no unicast connection is established.
    opti_multicast_ip : str, optional
        Multicast address to connect to.
    opti_port : int, optional
        Port of the Motive network interface.
    ssr_end_message : str, optional
        Symbol to terminate the XML message sent to SSR. By default, a binary zero.

    """
    # setting arguments if executed in command line
    if sys.argv[1:]:
        ssr_ip = str(sys.argv[1])
    if sys.argv[2:]:
        ssr_port = int(sys.argv[2])
    if sys.argv[3:]:
        ssr2_port = int(sys.argv[3])
    if sys.argv[4:]:
        opti_unicast_ip = str(sys.argv[4])
    if sys.argv[5:]:
        opti_multicast_ip = str(sys.argv[5])
    if sys.argv[6:]:
        opti_port = str(sys.argv[6])
    if sys.argv[7:]:
        ssr_end_message = str(sys.argv[7])

    # instantiation of the necessary class objects
    optitrack = opti_ssr.OptiTrackClient(opti_unicast_ip, opti_multicast_ip, opti_port)
    ssr = opti_ssr.SSRClient(ssr_ip, ssr_port, ssr_end_message)
    ssr2 = opti_ssr.SSRClient(ssr_ip, ssr2_port, ssr_end_message)
    localwfs = opti_ssr.LocalWFS(optitrack, ssr, ssr2)

    # creating sources once and continuously tracking position
    localwfs.start()

if __name__ == "__main__":
    demo()
