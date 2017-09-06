import itertools
from typing import Tuple, List

from IPy import IP

from . import ip


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


class NatRecord:
    def __init__(self, client_tun_ip: str, server_tun_ip: str,
                 client_addr: Address) -> None:
        self.client_tun_ip = client_tun_ip
        self.server_tun_ip = server_tun_ip
        self.client_addr = client_addr


class NAT:
    """
    Network Address Translator for packages going to and coming from TUN
    interface.
    """

    def __init__(self) -> None:
        self._records = {}

    def out(self, packet: bytearray, server_tun_ip: str,
            client_addr: Address) -> None:
        """Do NAT for outgoing packet.

        Changes packet source IP.
        """
        self._records[server_tun_ip] = NatRecord(
            ip.src_addr(packet),
            server_tun_ip,
            client_addr,
        )
        ip.set_src_addr(packet, server_tun_ip)

    def in_(self, packet: bytearray) -> Address:
        """Do NAT for incomming packet.

        Translates packet destination IP.

        Returns:
            Client socket address to which the packet should be forwarded to.
        """
        server_tun_ip = ip.dst_addr(packet)
        rec = self.record_by_server_tun_ip(server_tun_ip)
        ip.set_dst_addr(packet, rec.client_tun_ip)
        return rec.client_addr

    def record_by_server_tun_ip(self, server_tun_ip: str) -> NatRecord:
        if server_tun_ip in self._records:
            return self._records[server_tun_ip]
