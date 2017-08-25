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

from typing import List


def ip_from_str(ip: str) -> List[int]:
    return [int(n) for n in ip.split('.')]


def src_addr(packet: bytes) -> str:
    """Extracts src_addr field from IP packet."""
    return '.'.join([str(n) for n in packet[12:16]])


def set_src_addr(packet: bytearray, src_addr: str) -> None:
    addr = ip_from_str(src_addr)
    for i in range(12, 16):
        packet[i] = addr[i - 12]


def set_dst_addr(packet: bytearray, dst_addr: str) -> None:
    addr = ip_from_str(dst_addr)
    for i in range(16, 20):
        packet[i] = addr[i - 16]
