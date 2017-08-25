import socket
from threading import Thread
import logging

from . import tun, ip


class Server:
    def __init__(self, bind_port: int, bind_addr: str='0.0.0.0') -> None:
        self._sock = socket.socket()
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._addr = (bind_addr, bind_port)
        self._threads = []
        self._tun_dev = None

        self.last_conn = None
        self.orig_src_addr = None

    def route_traffic_to(self, tun_dev: tun.Device) -> 'Server':
        self._tun_dev = tun_dev
        return self

    def start(self) -> None:
        self._sock.bind(self._addr)
        self._sock.listen(65535)

        self._tun_read_thread = Thread(target=self.on_tun_recv)
        self._tun_read_thread.start()

        while True:
            conn, _ = self._sock.accept()
            new_thread = Thread(target=self.handle_connection, args=(conn,))
            self._threads.append(new_thread)
            new_thread.start()

    def on_tun_recv(self) -> None:
        while True:
            data = bytearray(self._tun_dev.read())
            logging.debug('tun0 recv: %s', data)

            client_conn = self._conn_by_dest(ip.dst_addr(data))
            if client_conn is not None:
                ip.set_dst_addr(data, self.orig_src_ip)
                logging.debug('conn send: %s', data)
                client_conn.send(data)

    def handle_connection(self, conn: socket.socket) -> None:
        logging.debug('New connection: %s', conn)
        self.last_conn = conn
        while True:
            packet = conn.recv(4096)
            if len(packet) == 0:
                break

            self.on_packet(packet, conn)

    def on_packet(self, packet: bytes, conn: socket.socket) -> None:
        packet = bytearray(packet)
        self.orig_src_ip = ip.src_addr(packet)
        new_src_ip = self._tun_ip_for(conn)
        ip.set_src_addr(packet, new_src_ip)

        logging.debug('tun0 send: %s', packet)
        self._tun_dev.write(packet)

    def _tun_ip_for(self, conn: socket.socket) -> str:
        # TODO: assign IP by connection.
        return '10.0.0.2'

    def _conn_by_dest(self, ip: str) -> socket.socket:
        if ip == '10.0.0.2':
            return self.last_conn
