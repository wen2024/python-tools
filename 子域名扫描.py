import os


# 基于Ping命令的子域名扫描
import socket


def ping_domain():
    with open("../dict/main.txt") as file:
        domain_list = file.readlines()

    for domain in domain_list:
        result = os.popen(f'ping -n 1 -w 1000 {domain.strip()}.woniuxy.com').read()
        # print(result)
        if "请求超时" in result or "TTL=" in result:
            print(f"{domain.strip()}.woniuxy.com")

        if "找不到主机" not in result:
            print(f"{domain.strip()}.woniuxy.com")

# 基于socket库的DNS解析功能实现扫描
def socket_domain():
    with open("../dict/main.txt") as file:
        domain_list = file.readlines()

    for domain in domain_list:
        try:
            # 有效
            ip = socket.gethostbyname(f'{domain.strip()}.woniuxy.com')
            print(f'{domain.strip()}.woniuxy.com  的ip为：{ip}')
        except socket.gaierror:
            pass


if __name__ == "__main__":
    # ping_domain()
    socket_domain()
