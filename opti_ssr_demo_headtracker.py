"""
A python module for demonstrating head orientation tracking for binaural
synthesis.

Usage: python opti_ssr_demo.py [SSR_IP] [SSR_port] [optitrack ip] [multicast address] [optitrack port] [end_message]
"""

import sys
import opti_ssr

def demo(ssr_ip='localhost', ssr_port=4711, opti_unicast_ip=None, opti_multicast_ip='239.255.42.99', opti_port=1511, ssr_end_message='\0'):
    """ #todo

    Parameters
    ----------
    ssr_ip : str, optional
        IP of the server running thr SSR.
    ssr_port : int, optional
        Port of SSR Network Interface. By default, port 4711.
    opti_unicast_ip : str, optional
        IP of the Motive software to establish a unicast connection to.
        By default, no unicast connection is established.
    opti_multicast_ip : str, optional
        Multicast address to connect to.
    opti_port : int, optional
        Port of the Motive network interface.
    ssr_end_message : str, optional
        Symbol to terminate the XML messages send to SSR. By default, a binary zero.

    """
    # setting arguments if executed in command line
    if sys.argv[1:]:
        ssr_ip = str(sys.argv[1])
    if sys.argv[2:]:
        ssr_port = int(sys.argv[2])
    if sys.argv[3:]:
        opti_unicast_ip = str(sys.argv[3])
    if sys.argv[4:]:
        opti_multicast_ip = str(sys.argv[4])
    if sys.argv[5:]:
        opti_port = str(sys.argv[5])
    if sys.argv[6:]:
        ssr_end_message = str(sys.argv[6])

    # instantiation of the necessary class objects
    optitrack = opti_ssr.OptiTrackClient(opti_unicast_ip, opti_multicast_ip, opti_port)
    ssr = opti_ssr.SSRClient(ssr_ip, ssr_port, ssr_end_message)
    headtracker = opti_ssr.HeadTracker(optitrack, ssr)

    # continuous tracking of head orientation
    headtracker.start()

if __name__ == "__main__":
    demo()
