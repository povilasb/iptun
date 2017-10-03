from hamcrest import assert_that, is_, equal_to
from dnslib import DNSRecord

from iptun.dns import _max_data_len, EncodeDataToRequest, \
    decode_data_from_request, _data_to_dns_name


def describe_max_data_len():
    def it_exludes_dns_name_suffix_and_dots_from_max_dns_name_length():
        max_dlen = _max_data_len('tun.example.com')

        assert_that(max_dlen, is_(231))


def describe_data_to_dns_name():
    def it_returns_base32_encoded_data_and_split_into_chunks_with_max_63_symbols():
        data = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        data += data

        dns_name = _data_to_dns_name(data)

        assert_that(
            dns_name,
            is_('MFRGGZDFMZTWQ2LKNNWG23TPOBYXE43UOV3HO6DZPJAUEQ2EIVDEOSCJJJ'\
                'FUYTK.OJ5IFCUSTKRKVMV2YLFNGCYTDMRSWMZ3INFVGW3DNNZXXA4LSON2'\
                'HK5TXPB4XUQ.KCINCEKRSHJBEUUS2MJVHE6UCRKJJVIVKWK5MFSWQ=')
        )


def describe_decode_data_from_request():
    def describe_when_valid_dns_query_is_provided():
        def it_decodes_data_from_query_name():
            orig_data = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            orig_data = orig_data + orig_data
            dns_query = EncodeDataToRequest('tun.example.com').to_dns_query(orig_data)

            decoded = decode_data_from_request(dns_query, 'tun.example.com')

            assert_that(decoded, equal_to(orig_data))
