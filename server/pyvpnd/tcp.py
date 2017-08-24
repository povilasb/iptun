import socket
from threading import Thread

from . import tun


class Server:
    def __init__(self, bind_port: int, bind_addr: str='0.0.0.0') -> None:
        self._sock = socket.socket()
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._addr = (bind_addr, bind_port)
        self._threads = []
        self._tun_dev = None

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
            data = self._tun_dev.read()
            print('tun0 recv:', data)

    def handle_connection(self, conn: socket.socket) -> None:
        print('New connection:', conn)
        while True:
            packet = conn.recv(4096)
            if len(packet) == 0:
                break

            print('tun0 send:', packet)
            self._tun_dev.write(packet)
