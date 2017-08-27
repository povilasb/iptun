from threading import Thread
import socket

from . import tun


def main() -> None:
    tun_dev = tun.Device('tun1', '10.1.0.1')
    tun_dev.up()

    server_sock = socket.socket()
    server_sock.connect(('192.168.0.100', 3000))

    read_thread = Thread(target=on_response, args=(tun_dev, server_sock,))
    read_thread.start()

    while True:
        packet = tun_dev.read()
        server_sock.send(packet)

    read_thread.join()
    server_sock.close()


def on_response(tun_dev: tun.Device, server_sock: socket.socket) -> None:
    while True:
        packet = server_sock.recv(4069)
        tun_dev.write(packet)


if __name__ == '__main__':
    main()
