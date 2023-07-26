"""************************************
*  Exe 7 - SYNflood ,nadav zimmerman  *
************************************"""
"""
הנחות היסוד לגילוי הip החשודים:
א. הip החשודים ישלחו syn - התנאי החשוב וההכרחי ביותר.
ב. הip החשודים לא ישלחו ack, הם רק מעוניינים להכביד וליצור עומס על השרתים לכן לא ישלחו ack לפי פרוטוקול לחיצת הידיים.
ג.שהip החשודים יפנו לip רבים ככל הניתן.
ד. הip החשודים יקבלו פניות (dst) מעטות.
הערה - את היחס רבים הגדרתי כגדולים או שווים ל10, ואת היחס מעטים הגדרתי כ10 ומטה.

הבדיקות שביצעתי:
א. מספר הsyn ששלח כל ip
ב. מספר הack ששלח כל ip
ג. מספר כתובות הip אליהם שלח הip בקשות/תגובות
ד. מספר כתובות הip מהם קיבל הip בקשות/תגובות
"""
from scapy.all import *

PCAP_PATH = r"C:\Networks\work\exercise_7_rambam -tcp\SYNflood.pcap"
WRITE_PATH = r"C:\Networks\work\exercise_7_rambam -tcp\SYNflood_result_nadav_zimmerman.txt"
STANDARD_UNIT = 10

def main():
    packets = rdpcap(PCAP_PATH)

    # empty list to store the IP addresses of the attackers
    attackers = []
    # Initialize counters for this IP address
    send_syn_count = {}
    send_ack_counts = {}
    req_rcv = {}
    req_snd = {}
    print(len(packets))
    counter = 0   # only to see the progress of the program

    # Iterate through the file
    for packet in packets:
        counter += 1
        if not counter % 1000:
            print(counter)

        # Check if the packet is a TCP packet
        if TCP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            # Check if the source IP address is already in the list
            if src_ip not in attackers:
                # If not, add it to the list
                attackers.append(src_ip)

            # Increment the source ip count
            if src_ip in req_snd:
                req_snd[src_ip] += 1
            else:
                req_snd[src_ip] = 1

            # Increment the destination ip count
            if dst_ip in req_rcv:
                req_rcv[dst_ip] += 1
            else:
                req_rcv[dst_ip] = 1

            # Increment the syn count (only syn without ack)
            if packet[TCP].flags & 0x02 and not packet[TCP].flags & 0x10:
                if src_ip in send_syn_count:
                    send_syn_count[src_ip] += 1
                else:
                    send_syn_count[src_ip] = 1

                # Increment the ack count (include syn ack)
            if packet[TCP].flags & 0x10:
                if src_ip in send_ack_counts:
                    send_ack_counts[src_ip] += 1
                else:
                    send_ack_counts[src_ip] = 1

    res = ''
    for suspect in attackers:
        if suspect in send_syn_count and send_syn_count[suspect] >= STANDARD_UNIT:
            if suspect not in send_ack_counts or send_ack_counts[suspect] <= STANDARD_UNIT:
                if suspect not in req_rcv or req_rcv[suspect] <= STANDARD_UNIT:
                    if suspect in req_snd and req_snd[suspect] >= STANDARD_UNIT:
                        res += suspect + '\n'
    f = open(WRITE_PATH, 'w')
    f.writelines(res)


if __name__ == '__main__':
    main()
