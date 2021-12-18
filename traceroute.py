import argparse
import time

from scapy.sendrecv import sr1
from scapy.layers.inet import IP, TCP, ICMP, UDP
from scapy.volatile import RandShort
from scapy.layers.inet6 import IPv6
from ipwhois import IPWhois, IPDefinedError


class Traceroute:
    def __init__(self):
        input_data = self._create_parser()
        self.ip = input_data.IP_ADDRESS
        self.timeout = input_data.t
        self.verbose = input_data.v
        self.protocol = input_data.protocol
        self.num = input_data.n
        self.port = input_data.p

    # region input
    @staticmethod
    def _create_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('IP_ADDRESS', help='ip for check', type=str, action='store')
        parser.add_argument('-t', default=2, type=float, help='response timeout (default 2s)')
        parser.add_argument('-v', action='store_true', default=False,
                            help='displaying the autonomous system number for each ip address')
        parser.add_argument('-p', type=int, action='store', help='port (for tcp or udp)', required=True)
        parser.add_argument('-n', type=int, action='store', default=30, help='maximum number of requests')
        parser.add_argument('protocol', type=str, action='store', help='protocol{tcp|udp|icmp}',
                            choices=['tcp', 'udp', 'icmp'])
        return parser.parse_args()

    # endregion

    def find_route(self):
        package_maker = self._protocol_manager()
        for num_ttl in range(1, self.num + 1):
            start_time = time.perf_counter()
            ans = sr1(package_maker(num=num_ttl), verbose=0, timeout=self.timeout)
            elapsed_time = time.perf_counter() - start_time
            self._handle_output(ans=ans, elapsed_time=elapsed_time, num_ttl=num_ttl)
            if ans and ans.src == self.ip:
                break

    # package region
    def _create_tcp_package(self, num):
        if ':' in self.ip:
            return IPv6(dst=self.ip, hlim=num) / TCP(dport=self.port, flags='S')
        return IP(dst=self.ip, ttl=num) / TCP(dport=self.port, flags='S')

    def _create_udp_package(self, num):
        if ':' in self.ip:
            return IPv6(dst=self.ip, hlim=num) / UDP(dport=self.port, sport=RandShort())
        return IP(dst=self.ip, ttl=num) / UDP(sport=RandShort(), dport=self.port)

    def _create_icmp_package(self, num):
        if ':' in self.ip:
            return IPv6(dst=self.ip, hlim=num) / ICMP()
        return IP(dst=self.ip, ttl=num) / ICMP()

    def _protocol_manager(self):
        if self.protocol == 'tcp':
            return self._create_tcp_package
        elif self.protocol == 'udp':
            return self._create_udp_package
        elif self.protocol == 'icmp':
            return self._create_icmp_package
        else:
            raise ValueError('incorrect protocol')

    # endregion

    def _handle_output(self, ans, elapsed_time, num_ttl):
        if ans is None:
            print(f'{num_ttl} *')
            return
        if self.verbose:
            _as = self._get_asn(ans.src)
            print(f'{num_ttl} {ans.src} {int(elapsed_time * 1000)}ms {_as}')
        else:
            print(f'{num_ttl} {ans.src} {int(elapsed_time * 1000)}ms')

    def _get_asn(self, ip):
        try:
            return IPWhois(ip).lookup_whois()['asn']
        except IPDefinedError:
            return '--'


def main():
    traceroute = Traceroute()
    traceroute.find_route()


if __name__ == '__main__':
    main()
