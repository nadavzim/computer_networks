from scapy.all import *

SITE_URL = '8.8.8.8'
NO_RSPN = "no respone"


def main():
    i = 1
    while True:
        trace_route = IP(dst=SITE_URL, ttl=i)/ICMP()/'my trace route!'
        try:
            trace_respone = sr1(trace_route, verbose=0, timeout=1)
            print("hoop number ", i, ": ", trace_respone[IP].src)
            if trace_respone[ICMP].type == 0:
                break
        except:
            print(NO_RSPN)
        i += 1


if __name__ == "__main__":
    # Call the main handler function
    main()
