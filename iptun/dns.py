"""Utilities to encode/decode arbitrary data to DNS queries."""

import math
import random
import base64
import string

from dnslib import DNSRecord, QTYPE, TXT, RR


class EncodeError(Exception):
    pass


class EncodeDataToRequest:
    """Encodes arbitrary data to DNS request."""

    def __init__(self, dns_suffix: str) -> None:
        self._dns_suffix = dns_suffix
        self._max_data_len = _max_data_len(dns_suffix)

    def to_dns_query(self, data: bytes) -> DNSRecord:
        return DNSRecord.question(self.to_str(data), qtype='TXT')

    # TODO: compress data before encoding to base32
    def to_str(self, data: bytes) -> str:
        str_data = _data_to_dns_name(data)
        self._ensure_data_fits(str_data)

        nonce = '{}{}'.format(
            random.choice(string.ascii_lowercase), random.randint(0, 9))
        return '{}.{}.{}'.format(str_data, nonce, self._dns_suffix)

    def _ensure_data_fits(self, data: bytes) -> None:
        if len(data) > self._max_data_len:
            raise EncodeError('Data will not fit into DNS name')


def _data_to_dns_name(data: bytes) -> str:
    b32 = base64.b32encode(data).decode('ascii')
    return '.'.join(map(lambda i: b32[i:i+63], range(0, len(b32), 63)))


def _max_data_len(dns_suffix: str) -> int:
    max_dns_name_len = 254
    remaining_len = max_dns_name_len - len(dns_suffix) - 4
    return remaining_len - math.ceil(remaining_len / 64)


def decode_data_from_request(dns_rec: DNSRecord, dns_suffix: str) -> bytes:
    query_name = str(dns_rec.questions[0].qname)
    rm_last_chars = len(dns_suffix) + 4
    query_name = query_name[:-rm_last_chars]
    data_parts = query_name.split('.')
    return base64.b32decode(''.join(data_parts))


def encode_data_to_response(record: DNSRecord, data: bytes) -> DNSRecord:
    resp = record.reply()
    query_name = record.questions[0].qname
    txt_data = str(base64.b64encode(data))
    resp.add_answer(RR(query_name, QTYPE.TXT, rdata=TXT(txt_data), ttl=60))
    return resp
