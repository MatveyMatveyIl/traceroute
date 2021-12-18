# traceroute
traceroute with the ability to send packets ICMP, TCP or UDP.

## Install

```pip install -r requirements.txt```

## Usage

### help
``sudo python3 -m traceroute -h``

### example
`` sudo python3 -m traceroute -p 53 1.1.1.1 tcp``

## Features
- Timeout
- maximum number of requests
- verbose mode to ASN
- The following protocols are defined
  - `UDP` `TCP` `ICMP`
- using scapy
- IPv6 support

## Author
### Ilichev Matvey 
