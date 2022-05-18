import requests
import string
import random

# 生成数字大小写字母的字符串
strs = string.ascii_letters + string.digits
# 用于生成随机字符串
ran_str = ''.join(random.sample(strs, 4))
# 给定输入点
# inp = "http://192.168.100.50/xss/level1.php?name=test"
inp = "http://192.168.100.50/xss/level2.php?keyword=test"
# inp = "http://192.168.100.50/xss/level3.php?keyword=222"

# 处理url
url = inp.split("?")[0]
param = inp.split("?")[1].split("=")[0]


# 确定输出点,进行试探
def output():
    # 定义特殊字符列表
    define = {"chr": ">", "single": "'", "double": "\""}
    res = requests.get(url=url, params={param: ran_str})
    # 去除空格，方便匹配
    data = "".join(res.text.split("\n"))
    # print(data)
    start = data.find(ran_str)  # 输入点的起始位置
    if start == -1:
        print("该页面没有输出点。")
    else:
        i = 1
        # 判断左边界
        while True:
            for k, v in define.items():
                if data[start+i] == v:
                    return k  # 返回输出点的类型
                i += 1

def xss_scan():
    # 遍历字典
    with open('../dict/xss-20.txt') as file:
        payload_list = file.readlines()

    for payload in payload_list:
        res = requests.get(url=url, params={param: payload.strip()})
        if res.text.find(payload.strip()) > 0:
            print(f"疑似注入点, payload为: {payload.strip()}")


if __name__ == '__main__':
    xss_scan()
