"""
A module to establish a TCP IP4 network connection and send XML messages to communicate with SSR
"""
from __future__ import print_function
import socket

class ssr_network:
    """ #todo

    Attributes
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

    def __init__(self, IP='139.30.207.123', port=4711, end_message='/0'):
        self._ip = IP
        self._port = port
        self._end_message = end_message

        #IP4 and TCP connection
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((self._ip, self._port))

    def __del__(self):
        self._s.close()
        print("ssr_network: socket closed")

    def src_creation(self, src_id):
        """
        creating the XML message for defining a new source in SSR
        """
        new_src = '<request><source new="true" id="{0}" port="0"></source></request>'.format(src_id)+self._end_message
        self._s.send(new_src.encode())


    def src_position(self, src_id, x, y):
        """
        creating the XML message for changing name and position of an existing source in SSR
        """
        # z-coordinate of Motive is the y-coordinate of the SSR
        position = '<request><source id="{0}" name="SourceMotive{0}"><position x="{1:4.2f}" y="{2:4.2f}"/></source></request>'.format(src_id, x, y)+self._end_message
        self._s.send(position.encode())


