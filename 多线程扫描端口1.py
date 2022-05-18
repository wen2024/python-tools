import re
import threading
import socket


def port_main():
    ip = input("请输入目标ip: ")
    check_ip = re.match(  # 效验ip地址
        "^(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\."
        "(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])$", ip)
    if check_ip:
        sp = ScanPort(ip)
        sp.use()
    else:
        print("IP格式不合法，请重新输入！")
        port_main()


class ScanPort:
    # 接收扫描的ip和线程数，进程默认为4，每个进程的线程默认2000
    def __init__(self, ip, thread=10000):
        # 常用端口列表
        self.common_port = [7, 21, 22, 23, 25, 43, 53, 67, 68, 69, 79, 80, 81, 88, 109, 110, 113, 119, 123, 135, 137,
                            138,
                            139,
                            143, 161, 162, 179, 194, 220, 389, 443, 445, 465, 513, 520, 520, 546, 547, 554, 563, 631,
                            636,
                            991, 993,
                            995, 1080, 1194, 1433, 1434, 1494, 1521, 1701, 1723, 1755, 1812, 1813, 1863, 3269, 3306,
                            3307,
                            3389,
                            3544,
                            4369, 5060, 5061, 5355, 5432, 5671, 5672, 6379, 7001, 8080, 8081, 8088, 8443, 8883, 8888,
                            9443,
                            9988,
                            9988, 15672, 50389, 50636, 61613, 61614]
        self.ip = ip
        self.thread = thread  # 线程数
        self.port_list = []  # 存放可用的端口

    # 先扫经常使用的端口
    def use(self):
        for port in self.common_port:
            threading.Thread(target=self.scan, args=(port,)).start()
        self.resource()

    # 线程分配
    def resource(self):
        # 开启线程
        thread = []
        # 每个线程数扫描的端口数
        port_count = int(65535 / self.thread) + 1
        for port in range(1, 65535, port_count):
            t = threading.Thread(target=self.comm_port, args=(port, port_count))
            t.start()
            thread.append(t)
        for t in thread:
            t.join()

    def comm_port(self, start, port_count):
        for i in range(start, start + port_count):
            if i in self.common_port:
                continue
            if i > 65535:
                break
            self.scan(i)

    # 扫描端口
    def scan(self, port):
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((self.ip, port))
            # print(f"端口: {port}可用。")
            s.close()
            self.port_list.append(port)
        except Exception as e:
            pass

    def __del__(self):
        self.port_list.sort()  # 排序
        print(f"{self.ip} 可用端口: {self.port_list}\n")
