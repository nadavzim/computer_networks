from scapy.all import *
import ipaddress


def encrypt_by_port():
    """encrypt msg using ports"""
    msg = input("enter the msg you want to encrypt: ")
    for c in msg:
        pckt = IP('127.0.0.1')/UDP(sport=1000, dport=ord(c))
        send(pckt)


def my_dns(site, op_code=0):
    try:
        res = ''
        if op_code == 0:
            dns_req = IP(dst='8.8.8.8')/UDP(sport=2000, dport=53)/DNS(qdcount=1)/DNSQR(qname=site)
            dns_rcv = sr1(dns_req, verbose=0)
            for i in range(0, dns_rcv[DNS].ancount):
                try:
                    return_ip = dns_rcv[DNSRR][i].rdata
                    if ipaddress.ip_address(return_ip):
                        res += return_ip + '\n'
                except ValueError:
                    continue
        else:
            site = ipaddress.ip_address(site).reverse_pointer
            dns_req = IP(dst='8.8.8.8')/UDP(dport=53)/DNS(qdcount=1, )/DNSQR(qname=site, qtype='PTR')
            dns_rcv = sr1(dns_req, verbose=0)
            dns_rcv.show()
            res = dns_rcv[DNSRR].rdata
        return res  # res[DNSRR].rdata
    except:
        return 'error'


def triple_hand_shake_():
    syn_segment = TCP(sport=8120, dport=80, seq=123, flags='S')
    syn_packet = IP(dst='www.google.com') / syn_segment
    syn_ack_packet = sr1(syn_packet, verbose=0)
    ack_segment = TCP(sport=8120, dport=80, ack=syn_ack_packet[TCP].seq+1, seq=124, flags='A')
    ack_packet = IP(dst='www.google.com')/ack_segment
    send(ack_packet)


def find_open_ports(site_url, start, end):
    """check if ports 10-20 are ready to connect"""
    res_list = []
    for i in range(start, end):
        syn_segment = TCP(sport=8120, dport=80, seq=123, flags='S')
        syn_packet = IP(dst=site_url) / syn_segment
        try:
            ack_packet = sr1(syn_packet, verbose=0, timeout=2)
            ack_packet.show()
            if A in ack_packet[TCP].flags:
                res_list.append(f'port {i}')
        except:
            continue
    return res_list


def multy_ping():
    packets = []
    n = input("enter a number of ping's: ")
    ip = input("enter a ip for the ping: ")
    print(f'sending {n} packet\'s to {ip}')
    for i in range(0, int(n)):
        request_packet = IP(dst=ip) / ICMP(type="echo-request") / f"ping number {i+1}"
        res = sr1(request_packet, verbose=0, timeout=1)
        if res is not None:
            packets.append(res)
    print(f'got reply from {len(packets)} packet\'s')


if __name__ == "__main__":
    # print(my_dns('www.youtube.com'), my_dns('8.8.8.8').decode(), end='\n')  # dns server

    # triple_hand_shake_()

    # print(find_open_ports('', 78, 82))

    # multy_ping()