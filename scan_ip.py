import os
import re
import threading
from random import randint

from scapy.layers.l2 import ARP
from scapy.sendrecv import sr1
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

ip_list = []

# ARP扫描
def scapy_ip(last, ip):
    three = '.'.join(ip.split('.')[:-1])
    ip = f'{three}.{last}'
    try:
        source = f"{three}.{randint(1, 254)}"  # 随机源ip
        pkg = ARP(psrc=source, pdst=ip)
        reply = sr1(pkg, timeout=2, verbose=False)
        mac = reply[ARP].hwsrc
        print(f"IP地址: {ip}, MAC地址: {mac}")
        ip_dict = {"ip": ip, 'mac': mac}
        ip_list.append(ip_dict)
    except Exception as e:
        pass

# Ping命令扫描
def ping_ip(last, ip):
    three = '.'.join(ip.split('.')[:-1])
    ip = f'{three}.{last}'
    try:
        output = os.popen(f"ping -n 1 -w 3 {ip} | findstr TTL=").read()
        if len(output) > 0:
            print(f"{ip} 在线。")
            ip_list.append(ip)
    except Exception as e:
        pass


def select(func):
    ip = input("请输入你的内网ip: ")
    check_network = re.match(  # 效验ip地址
        "^(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\."
        "(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])", ip)

    if check_network:  # 判断格式
        print("开始扫描。")
        thread = []
        for last in range(0, 256):
            t = threading.Thread(target=func, args=(last, ip))
            t.start()
            thread.append(t)
        for i in thread:
            i.join()

        print(f"扫描结果: {ip_list}")

    else:
        print("ip格式错误")

def ip_main():
    while True:
        common = input("1、ARP扫描  2、Ping命令扫描  3、退出\n请输入序号: ")
        if common == '1':
            select(scapy_ip)
        elif common == '2':
            select(ping_ip)
        elif common == '3':
            break
        else:
            print("输入错误。")





