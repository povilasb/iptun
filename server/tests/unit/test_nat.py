from hamcrest import assert_that, is_

from iptund import net

from pypacker.layer3.ip import IP


def describe_NAT():
    def describe_out():
        def it_changes_packet_source_address_to_server_tun_ip():
            nat = net.NAT()
            bin_packet = bytearray(
                IP(src_s='10.1.0.2', dst_s='8.8.8.8', p=1).bin())

            nat.out(bin_packet, '10.0.0.2', ('1.2.3.4', 65432))

            packet = IP(bin_packet)
            assert_that(packet.src_s, is_('10.0.0.2'))

    def describe_record_by_server_tun_ip():
        def describe_when_record_by_such_ip_exists():
            def it_returns_that_record():
                nat = net.NAT()
                bin_packet = bytearray(
                    IP(src_s='10.1.0.2', dst_s='8.8.8.8', p=1).bin())
                nat.out(bin_packet, '10.0.0.2', ('1.2.3.4', 65432))
                bin_packet = bytearray(
                    IP(src_s='10.1.0.2', dst_s='86.1.2.3', p=1).bin())
                nat.out(bin_packet, '10.0.0.3', ('1.2.3.5', 54321))

                r = nat.record_by_server_tun_ip('10.0.0.3')
                assert_that(r.client_tun_ip, is_('10.1.0.2'))
                assert_that(r.server_tun_ip, is_('10.0.0.3'))
                assert_that(r.client_addr, is_(('1.2.3.5', 54321)))
