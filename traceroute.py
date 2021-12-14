import argparse


class Traceroute:
    def __init__(self):
        input_data = self._create_parser()
        self.ip = input_data.IP_ADDRESS
        self.timeout = input_data.t
        self.verbose = input_data.v
        self.protocol = input_data.protocol
        self.num = input_data.n

    # region input
    @staticmethod
    def _create_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('IP_ADDRESS', help='ip for check', type=str, action='store')
        parser.add_argument('-t', default=2, type=float, help='response timeout (default 2s)')
        parser.add_argument('-v', action='store_true', default=False,
                            help='displaying the autonomous system number for each ip address')
        parser.add_argument('-p', type=int, action='store', help='port (for tcp or udp)')
        parser.add_argument('-n', type=int, action='store', default=20, help='maximum number of requests')
        parser.add_argument('protocol', type=str, action='store', help='protocol{tcp|udp|icmp}')
        return parser.parse_args()

    # endregion

    def find_route(self):
        for i in range(1, self.num):
            pass


def main():
    traceroute = Traceroute()
    traceroute.find_route()


if __name__ == '__main__':
    main()
