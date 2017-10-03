from hamcrest import assert_that, is_

from iptun import net


def describe_make_ip_range():
    def it_returns_list_of_ips_in_the_specified_subnet_without_first_two_addresses():
        ips = net.make_ip_range('1.2.3.252/30')

        assert_that(ips, is_(['1.2.3.254', '1.2.3.255',]))
