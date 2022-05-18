# 屏蔽警告信息
import logging
import threading

from scapy.layers.l2 import ARP
from scapy.sendrecv import sr1

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def scapy_ip(start):
    # print(start, start+5)
    # print(threading.currentThread().getName() + ": " + time.strftime("%Y-%m-%d %H:%M:%S"))

    # 每个线程处理5个扫描任务
    for j in range(start, start + 5):
        ip = f'192.168.18.{j}'
        try:
            pkg = ARP(psrc='192.168.18.1', pdst=ip)
            reply = sr1(pkg, timeout=1, verbose=False)
            mac = reply[ARP].hwsrc
            print(f"IP地址: {ip}, MAC地址: {mac}")
        except Exception as e:
            pass


def main():
    # 分配51个线程,进行整个网段的扫描
    for i in range(1, 256, 5):
        threading.Thread(target=scapy_ip, args=(i,)).start()


if __name__ == '__main__':
    main()
