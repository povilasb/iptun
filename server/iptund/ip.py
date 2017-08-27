""" IP packet manipulation utilities.

https://tools.ietf.org/html/rfc791#section-3.1

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 0  |Version|  IHL  |Type of Service|          Total Length         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 4  |         Identification        |Flags|      Fragment Offset    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 8  |  Time to Live |    Protocol   |         Header Checksum       |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 12 |                       Source Address                          |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 16 |                    Destination Address                        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 20 |                    Options                    |    Padding    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""

from pypacker.layer3.ip import IP
from pypacker.layer3.ip6 import IP6


def packet_version(packet: bytes) -> int:
    return packet[0] >> 4


def parse_packet(data: bytes) -> IP:
    packet_ver = packet_version(data)
    if packet_ver == 4:
        packet = IP(data)
    elif packet_ver == 6:
        packet = IP6(data)
    else:
        raise Exception('Unsupported IP packet version: {packet_ver}')
    return packet


def src_addr(packet: bytes) -> str:
    """Extracts src_addr field from IP packet."""
    return '.'.join([str(n) for n in packet[12:16]])


def set_src_addr(packet: bytearray, src_addr: str) -> None:
    ip = IP(packet)
    ip.src_s = src_addr
    # TODO: find out how to avoid data copying
    for i, b in enumerate(ip.bin()):
        packet[i] = b


def dst_addr(packet: bytes) -> str:
    """Extracts src_addr field from IP packet."""
    return '.'.join([str(n) for n in packet[16:20]])


def set_dst_addr(packet: bytearray, dst_addr: str) -> None:
    ip = IP(packet)
    ip.dst_s = dst_addr
    # TODO: find out how to avoid data copying
    for i, b in enumerate(ip.bin()):
        packet[i] = b
