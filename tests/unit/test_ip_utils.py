from hamcrest import assert_that, is_

from pypacker.layer3.ip import IP

from iptun import ip


def describe_src_addr():
    def it_extracts_source_address_from_ip_packet():
        packet = IP(src_s='127.0.0.1', dst_s='192.168.0.1', p=1)

        src_addr = ip.src_addr(packet.bin())

        assert_that(src_addr, is_('127.0.0.1'))


def describe_set_src_addr():
    def it_changes_ip_packet_source_address():
        bin_packet = bytearray(IP(src_s='127.0.0.1', dst_s='192.168.0.1', p=1).bin())

        ip.set_src_addr(bin_packet, '8.8.8.8')

        packet = IP(bin_packet)
        assert_that(packet.src_s, is_('8.8.8.8'))


def describe_set_dst_addr():
    def it_changes_ip_packet_destination_address():
        bin_packet = bytearray(IP(src_s='127.0.0.1', dst_s='192.168.0.1', p=1).bin())

        ip.set_dst_addr(bin_packet, '8.8.8.8')

        packet = IP(bin_packet)
        assert_that(packet.dst_s, is_('8.8.8.8'))
