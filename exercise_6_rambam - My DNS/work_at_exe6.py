from scapy.all import *
p = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="95.100.205.185.in-addr.arpa", qtype="PTR"))
p.show()
ans = sr1(p, verbose=0)
ans.show()

if ans[DNS].qd.qtype == 16:
    print(ans[DNS].an.rdata)