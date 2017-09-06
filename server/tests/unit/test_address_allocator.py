from hamcrest import assert_that, is_, not_, equal_to, calling, raises

from iptund import net


def describe_AddrAllocator():
    def describe_new():
        def describe_when_ip_range_has_available_addresses():
            def it_returns_first_available_ip_address():
                addr_pool = net.AddrAllocator('1.2.3.0/24')

                ip = addr_pool.new(12345)

                assert_that(ip, is_('1.2.3.2'))

            def describe_when_client_ids_match():
                def it_returns_same_ips():
                    addr_pool = net.AddrAllocator('1.2.3.0/24')

                    ip1 = addr_pool.new(12345)
                    ip2 = addr_pool.new(12345)

                    assert_that(ip1, equal_to(ip2))

            def describe_when_client_ids_differ():
                def it_returns_different_ips():
                    addr_pool = net.AddrAllocator('1.2.3.0/24')

                    ip1 = addr_pool.new(12345)
                    ip2 = addr_pool.new(12346)

                    assert_that(ip1, not_(equal_to(ip2)))

        def describe_when_ip_range_has_no_available_addresses():
            def it_raises_exception():
                addr_pool = net.AddrAllocator('1.2.3.252/30')
                addr_pool.new(12345)
                addr_pool.new(12346)

                assert_that(
                    calling(addr_pool.new).with_args(12347),
                    raises(net.NoAddressesAvailable)
                )

    def describe_has_available_addrs():
        def describe_when_ip_range_has_no_available_addresses():
            def it_returns_false():
                addr_pool = net.AddrAllocator('1.2.3.252/30')
                addr_pool.new(12345)
                addr_pool.new(12346)

                more_addrs = addr_pool.has_available_addrs()

                assert_that(more_addrs, is_(False))
