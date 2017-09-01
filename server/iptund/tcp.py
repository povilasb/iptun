import socket
from threading import Thread
import logging
import itertools
from typing import Tuple

from IPy import IP

from . import tun, ip


UdpAddr = Tuple[str, int]


class ClientConnection:
    def __init__(self, sock: UdpAddr) -> None:
        self.sock = sock
        self.local_ip = None

    def capture_local_ip(self, packet: bytes) -> None:
        self.local_ip = ip.src_addr(packet)

    def __getattr__(self, name: str):
        return getattr(self.sock, name)


# TODO: test
class NAT:
    """Network Address Translation."""

    def __init__(self, ip_range: str) -> None:
        self._ips = [str(addr) for addr in
                     itertools.islice(IP(ip_range), 2, None)]
        self._allocated_ips = {}

    def alloc_addr_for(self, conn: socket.socket) -> str:
        if conn in self._allocated_ips:
            return self._allocated_ips[conn]
        # TODO: raise exception if no IPs are available anymore.
        new_ip = self._ips.pop(0)
        # NOTE: conn might not be deallocated because of this reference
        # Use weak reference or hash?
        self._allocated_ips[conn] = new_ip
        return new_ip

    def release_addr_for(self, conn: socket.socket) -> None:
        conn_ip = self._allocated_ips[conn]
        self._ips.insert(0, conn_ip)
        del self._allocated_ips[conn]

    def get_connection(self, ip_addr: str) -> socket.socket:
        for conn, addr in self._allocated_ips.items():
            if addr == ip_addr:
                return conn


class Server:
    def __init__(self, bind_port: int, bind_addr: str='0.0.0.0') -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._addr = (bind_addr, bind_port)
        self._threads = []
        self._tun_dev = None

        self._nat = NAT('10.0.0.0/24')

    def route_traffic_to(self, tun_dev: tun.Device) -> 'Server':
        self._tun_dev = tun_dev
        return self

    def start(self) -> None:
        self._sock.bind(self._addr)

        self._tun_read_thread = Thread(target=self.on_tun_recv)
        self._tun_read_thread.start()

        while True:
            packet, addr = self._sock.recvfrom(4096)
            conn = ClientConnection(addr)
            new_thread = Thread(target=self.on_packet, args=(packet, conn,))
            self._threads.append(new_thread)
            new_thread.start()

    def on_tun_recv(self) -> None:
        while True:
            data = self._tun_dev.read()
            logging.debug('tun0 recv: %s', data)

            packet = ip.parse_packet(data)
            client_conn = self._nat.get_connection(packet.dst_s)
            if client_conn is not None:
                packet.dst_s = client_conn.local_ip
                data = packet.bin()
                logging.debug('conn send: %s', data)
                self._sock.send_to(data, client_conn.sock)

    def on_packet(self, packet: bytes, conn: UdpAddr) -> None:
        packet = bytearray(packet)
        conn.capture_local_ip(packet)
        new_src_ip = self._nat.alloc_addr_for(conn)
        ip.set_src_addr(packet, new_src_ip)

        logging.debug('tun0 send: %s', packet)
        self._tun_dev.write(packet)
