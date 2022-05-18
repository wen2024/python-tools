from scapy.all import *
from scapy.layers.inet import IP, TCP


# TCP半连接探测端口
def syn_scan():
    list = [80, 8080, 443, 554, 3306, 6379, 100, 22, 21, 23, 8088]
    for port in list:
        try:
            pkg = IP(dst='192.168.100.30') / TCP(dport=port, flags="S", seq=12345)
            reply = sr1(pkg, timeout=1, verbose=False)
            # print(reply[TCP].flags)
            if reply[TCP].flags == 0x12:
                print(port)
        except:
            pass


def tcp_connect():
    sport = random.randint(10000, 20000)
    seq = random.randint(10000, 65000)
    # sport = RandShort()  # 或 RandNum(min, max)
    print(sport)
    dport = 554
    dst = '192.168.100.139'
    # 第一次和第二次
    answer = sr1(IP(dst=dst) / TCP(sport=sport, dport=dport, seq=seq, flags="S"), timeout=5)
    # sport = answer.dport
    seq = answer[TCP].ack
    ack = answer[TCP].seq + 1
    print(seq, ack)
    print(answer.haslayer(TCP))
    # 第三次
    sr1(IP(dst=dst) / TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags="A"), timeout=3)

    # 发数据包
    send(IP(dst=dst) / TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags="PA") / "Testing chengdu123")
    # send(IP(dst=dst)/TCP(sport=sport,dport=dport,seq=seq,ack=ack,flags=24)/"Testing")
    # answer = sr1(IP(dst=dst)/TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags="PA")/"Testing")
    # time.sleep(1)
    # print(answer[Raw].load)
    # time.sleep(3)

    # 单方面断开连接
    # sr1(IP(dst=dst)/TCP(sport=sport,dport=dport,seq=seq, ack=ack, flags="FA"),timeout=3)
    # FIN=IP(dst=dst)/TCP(sport=sport, dport=dport, flags="FA", seq=seq, ack=ack)
    # FINACK=sr1(FIN)
    # time.sleep(2)
    # LASTACK=IP(dst=dst)/TCP(sport=sport, dport=dport, flags="A", seq=FINACK.ack, ack=FINACK.seq + 1)
    # send(LASTACK)


if __name__ == '__main__':
    # syn_scan()
    # tcp_connection()
    tcp_connect()
