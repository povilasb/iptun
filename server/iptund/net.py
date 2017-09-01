import itertools
from typing import Tuple, List

from IPy import IP

Address = Tuple[str, int]


class NoAddressesAvailable(Exception):
    pass


class AddrAllocator:
    """Allocates TUN interface IP addresses to incoming clients."""

    def __init__(self, ip_range: str) -> None:
        """
        Args:
            ip_range: e.g. 10.0.0.0/24.
        """
        self._ips = make_ip_range(ip_range)
        self._allocated_ips = {}

    def has_available_addrs(self) -> bool:
        return len(self._ips) > 0

    def new(self, client_id: int) -> str:
        if client_id in self._allocated_ips:
            return self._allocated_ips[client_id]
        if not self.has_available_addrs():
            raise NoAddressesAvailable()

        new_ip = self._ips.pop(0)
        self._allocated_ips[client_id] = new_ip
        return new_ip

    def release(self, client_id: int) -> None:
        ip = self._allocated_ips[client_id]
        self._ips.insert(0, ip)
        del self._allocated_ips[client_id]


def make_ip_range(cidr_addrs: str) -> List[str]:
    return [str(addr) for addr in itertools.islice(IP(cidr_addrs), 2, None)]
