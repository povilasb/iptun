import os
from fcntl import ioctl
import struct

from pyroute2 import IPRoute


# Some constants from Linux kernel header if_tun.h
UNIX_TUNSETIFF = 0x400454ca
UNIX_IFF_TUN = 0x0001
UNIX_IFF_NO_PI = 0x1000


class Device:
    def __init__(self, name, addr: str) -> None:
        self.name = name
        self.addr = addr

        self._ftun = None

    def up(self) -> None:
        self._ftun = create_vnet_device(self.name)
        set_addr(self.name, self.addr)

    def read(self, n: int=1500) -> bytes:
        """
        Args:
            n: bytes to read.
        """
        return os.read(self._ftun, n)

    def write(self, data: bytes) -> None:
        os.write(self._ftun, data)


def create_vnet_device(name: str) -> int:
    """Creates TUN (virtual network) device.

    Returns:
        file descriptor used to read/write to device.
    """
    make_if_req = struct.pack('16sH', name.encode('ascii'),
                              UNIX_IFF_TUN | UNIX_IFF_NO_PI)
    fid = os.open('/dev/net/tun', os.O_RDWR)
    ioctl(fid, UNIX_TUNSETIFF, make_if_req)
    return fid


def set_addr(dev: str, addr: str) -> None:
    """Associate address with TUN device."""
    ip = IPRoute()
    idx = ip.link_lookup(ifname=dev)[0]
    ip.addr('add', index=idx, address=addr, prefixlen=24)
    ip.link('set', index=idx, state='up')
    ip.close()
