#!/bin/bash

echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j MASQUERADE
