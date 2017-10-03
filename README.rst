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

Server
======

First of all the server must be started::

    $ make pyenv
    $ sudo pyenv/bin/python -m iptun.server

Currently it's accepting packets over UDP port 3000.

Client
======

Once the server is ready to relay packets, we can start the client::

    $ make pyenv
    $ sudo pyenv/bin/python -m iptun.client

By default no routes are configured, they should be added manually.
E.g. to route all traffic through our tunnel, execute::

    $ sudo ip route add default via 10.1.0.1

To route traffic to specific destination, execute::

    $ sudo ip route add 1.2.3.4 via 10.1.0.1

References
==========

.. [f1] http://blog.povilasb.com/posts/linux-virtual-network-devices/
.. [f2] http://blog.povilasb.com/posts/linux-network-routing-table/
