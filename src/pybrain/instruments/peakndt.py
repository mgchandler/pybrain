"""
Module managing connections with instruments by PeakNDT, which are available in
the Bristol UNDT lab at the time of writing.
"""

from enum import Enum
from ipaddress import IPv4Address
import socket


class Micropulse:
    """
    Object for connecting to and managing communication with the PeakNDT
    Micropulse 5.
    """
    class AcquisitionMode(Enum):
        FMC = 1
        HMC = 2
        
        @classmethod
        def is_member(cls, s: str):
            return s in [mode.name for mode in cls]
        
        
    def __init__(
            self,
            ip_address: str | IPv4Address = '10.1.1.2',
            port: int = 1067,
            acquisition: str | AcquisitionMode = AcquisitionMode.HMC,
        ) -> None:
        
        # Handle IP checking externally
        self.ip_address = IPv4Address(ip_address)
        
        # Make sure port is valid
        self.port = int(port)
        if (self.port < 0) | (self.port > 65535):
            raise ValueError(f'Port number {self.port} is not in range [0, 65535]')
            
        # Attempt to connect to the device
        self._socket = socket.socket()
        self._socket.connect((str(self.ip_address), self.port))
            
        # Acquisition mode constrained to a few kinds.
        if isinstance(acquisition, str):
            try:
                acquisition = AcquisitionMode(acquisition)
            except KeyError:
                raise ValueError(f'Acqusition mode {acquisition} is not valid')
        elif not isinstance(acquisition, AcquisitionMode):
            raise ValueError(f'Acquisition mode {acquisition} is not valid')
        self.acquisition = acquisition
        
    
    def disconnect(self) -> None:
        if not self._socket._closed:
            self._socket.close()
        
    
    def __enter__(self):
        return self
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
    