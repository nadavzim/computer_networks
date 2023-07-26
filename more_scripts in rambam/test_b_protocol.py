
import sys
from scapy.all import *

SERVER_IP = '127.0.0.1'
PACKET_CODE = 32
TIMEOUT = 2
ADD = '+'
SUB = '-'
MULT = '*'
DIV = '/'


"""protocol"""


def calc_num(number):
    op = number[-1]
    number = number[:-1]
    half = int(len(number)/2)
    num1 = int(number[:half])
    num2 = int(number[half:])
    if op == ADD:
        res = str(num1 + num2)
    elif op == SUB:
        res = str(num1 - num2)
    elif op == MULT:
        res = str(num1 * num2)
    elif op == DIV:
        res = str(num1 / num2)
    return res


def filter_code(p):
    if ICMP in p:
        return p[ICMP].id == PACKET_CODE and p[ICMP].chksum == PACKET_CODE
