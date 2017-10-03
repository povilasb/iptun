from threading import Thread
import socket

from . import tun


def src_addr(packet: bytes) -> str:
    """Extracts src_addr field from IP packet."""
    return '.'.join([str(n) for n in packet[12:16]])


def main() -> None:
    server_addr = ('86.100.203.141', 3000)

    tun_dev = tun.Device('tun1', '10.1.0.1')
    tun_dev.up()

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    read_thread = Thread(target=on_response, args=(tun_dev, server_sock,))
    read_thread.start()

    while True:
        packet = tun_dev.read()
        print(src_addr(packet))
        # TODO: save packets to pcap file
        server_sock.sendto(packet, server_addr)

    read_thread.join()
    server_sock.close()


def on_response(tun_dev: tun.Device, server_sock: socket.socket) -> None:
    while True:
        packet, addr = server_sock.recvfrom(4069)
        tun_dev.write(packet)


if __name__ == '__main__':
    main()
