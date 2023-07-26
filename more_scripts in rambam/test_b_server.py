"""server"""
import sys
from scapy.all import *
import test_b_protocol as protocol

print("server up and running")
p = sniff(count=1, lfilter=protocol.filter_code)[0]
msg = p[0][Raw].load.decode()
res = protocol.calc_num(msg)
real_dst = dst = p[0][IP].src
fake_dst = protocol.SERVER_IP
packet = IP(fake_dst) / ICMP(type="echo-request", id=protocol.PACKET_CODE, chksum=protocol.PACKET_CODE) / res
send(packet)