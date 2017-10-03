=====
About
=====

This is some experiments with `IP tunneling
<https://en.wikipedia.org/wiki/IP_tunnel>`_ and Python.
I have intentions to implement IP over DNS, HTTP, ICMP, etc.


Overview
========

::

                           +---------+
                           | Routing |
                           |  table  |
                           +---------+
                               ^
                               | consults
    +--------+            +---------+
    |   IP   |  goes into | Network | forwards    +------+
    | packet | ---------> |  stack  | --------->  | tun0 |
    +--------+            +---------+             +------+
                            |     ^   encapsulated   |
                            |     +------------------+
                            V           packet
                        +------+
                        | eth0 |
                        +------+
                           |
    client                 |
    ------------------------------------------------------------------------
    server                 |
                           V
     +--------+         +------+  client  +--------+
     | Server | <------ | eth0 | -------> | Target |
     | daemon |         +------+  packet  | server |
     +--------+            ^              +--------+
        | decapsulated     |
        |   IP packet      |
        V                  |
    +------+ client    +---------+           +---------+
    | tun0 | --------> | Network | consults  | Routing |
    +------+ packet    |  stack  | --------> |  table  |
                       +---------+           +---------+

Where `tun0` is virtual network device.

References
==========

.. [f1] http://blog.povilasb.com/posts/linux-virtual-network-devices/
.. [f2] http://blog.povilasb.com/posts/linux-network-routing-table/
