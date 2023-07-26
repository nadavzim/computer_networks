
from scapy.all import *
syn_segment = TCP(dport=80, seq=123, flags='S')
syn_packet = IP(dst='1.1.1.1')/syn_segment
syn_ack_packet = sr1(syn_packet)
ack_segment = TCP(dport=80, ack=syn_ack_packet[TCP].seq+1, seq=syn_ack_packet[TCP].ack+1, flags='A')
ack_packet = IP(dst='1.1.1.1')/ack_segment
send(ack_packet)
