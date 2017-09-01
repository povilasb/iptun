import socket
from threading import Thread
import logging
import itertools
from typing import Tuple

from IPy import IP

from . import tun, ip, net


class Server:
    def __init__(self, bind_port: int, bind_addr: str='0.0.0.0') -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._addr = (bind_addr, bind_port)
        self._threads = []
        self._tun_dev = None

        self._nat = net.NAT()
        self._addr_allocator = net.AddrAllocator('10.0.0.0/24')

    def route_traffic_to(self, tun_dev: tun.Device) -> 'Server':
        self._tun_dev = tun_dev
        return self

    def start(self) -> None:
        self._sock.bind(self._addr)

        self._tun_read_thread = Thread(target=self.on_tun_recv)
        self._tun_read_thread.start()

        while True:
            packet, addr = self._sock.recvfrom(4096)
            new_thread = Thread(target=self.on_packet, args=(packet, addr,))
            self._threads.append(new_thread)
            new_thread.start()

    def on_tun_recv(self) -> None:
        while True:
            packet = bytearray(self._tun_dev.read())
            logging.debug('tun0 recv: %s', packet)

            client_addr = self._nat.in_(packet)
            if client_addr is not None:
                logging.debug('conn send: %s', packet)
                self._sock.send_to(packet, client_addr)

    def on_packet(self, packet: bytes, client_addr: net.Address) -> None:
        packet = bytearray(packet)

        new_tun_ip = self._addr_allocator.new(hash(client_addr))
        self._nat.out(packet, new_tun_ip, client_addr)

        logging.debug('tun0 send: %s', packet)
        self._tun_dev.write(packet)
