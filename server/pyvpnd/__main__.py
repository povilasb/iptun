from . import tcp, tun


def main() -> None:
    tun_dev = tun.Device('tun0', '10.0.0.1')
    tun_dev.up()

    server = tcp.Server(3000).route_traffic_to(tun_dev)
    server.start()


if __name__ == '__main__':
    main()
