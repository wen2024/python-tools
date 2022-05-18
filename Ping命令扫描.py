import os
import threading
import time

count = 0


def ping_ip(start):
    print(threading.currentThread().getName() + ": " + time.strftime("%Y-%m-%d %H:%M:%S"))
    # 每个线程处理5个扫描任务
    for j in range(start, start + 5):
        ip = f'192.168.18.{j}'
        output = os.popen(f'ping -n 1 -w 100 {ip} | findstr TTL=').read()
        if len(output) > 0:
            print(f"{ip} 在线！")
            global count
            count += 1


def main():
    # 分配51个线程,进行整个网段的扫描
    thread = []
    for i in range(1, 256, 5):
        t = threading.Thread(target=ping_ip, args=(i,))
        t.start()
        thread.append(t)
    '''
        主线程等待子线程结束
        为了让守护线程执行结束之后，主线程再结束，我们可以使用join方法，让主线程等待子线程执行
    '''
    for t in thread:
        t.join()

    print(f"总计有{count}个ip在线！")


if __name__ == '__main__':
    main()
