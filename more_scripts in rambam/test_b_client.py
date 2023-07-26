"""client"""

import sys
from scapy.all import *
import test_b_protocol as protocol

msg = sys.argv[1]
packet = IP(dst=protocol.SERVER_IP) / ICMP(type="echo-request", id=protocol.PACKET_CODE, chksum=protocol.PACKET_CODE) / msg
sr1(packet, timeout=protocol.TIMEOUT)
print(rcv[Raw].load)
