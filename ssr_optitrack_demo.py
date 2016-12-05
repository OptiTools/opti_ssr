
import sys
from time import sleep

import ssr_optitrack
from opti_network import opti_network
from ssr_network import ssr_network

def demo(IP='139.30.207.123', port=4711, end_message='\0'):
    """ #todo

    Parameters
    ----------
    IP : str, optional
        IP of the server running thr SSR.
    port : int, optional
        Port of SSR Network Interface. By default, port = 4711.
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
        N = int(sys.argv[3])
    if sys.argv[4:]:
        R = float(sys.argv[4])
    if sys.argv[5:]:
        end_message = str(sys.argv[5])


    optitrack = opti_network()
    ssr = ssr_network(IP, port)
    ssr.src_creation(0)
    headtracker = ssr_optitrack.HeadTracker(optitrack, ssr)
    headtracker.start()

if __name__ == "__main__":
    demo()

