import requests
import urllib3
import signal
import time
import os

# 禁用警告
urllib3.disable_warnings()

# 基础URL和输出文件
base_url = 'https://esercenti.luckyred.it/film/'
output_file = 'valid_urls.txt'  # 输出文件名
start_point_config = 'start_point.config'  # 配置文件名
temp_file = 'temp_urls.txt'  # 临时文件名
max_length = 20  # 设置最大组合长度
max_execution_time = 5 * 3600  # 设置最大执行时间为5小时

def generate_combinations(prefix, length, valid_prefixes):
    if not valid_prefixes:
        return []
    combinations = []
    for char in '-abcdefghijklmnopqrstuvwxyz':
        for valid_prefix in valid_prefixes:
            new_prefix = valid_prefix + char
            if len(new_prefix) == length:
                combinations.append(new_prefix)
    return combinations

def check_url(url):
    response = requests.get(url, verify=False)
    return response.status_code == 200

def write_valid_url(url):
    with open(output_file, 'a') as file:
        file.write(url + '\n')
    print(f"Found valid URL: {url}")
    # 将有效的URL写入临时文件
    with open(temp_file, 'a') as file:
        file.write(url + '\n')

def timeout_handler(signum, frame):
    raise Exception("Execution time limit reached")

# 读取start_point.config文件获取start_point
with open(start_point_config, 'r') as file:
    start_point = file.read().strip()

# 设置定时器
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(max_execution_time)

try:
    # 初始化有效前缀列表
    valid_prefixes = [start_point]

    # 生成所有可能的字母组合
    for length in range(len(start_point), max_length + 1):
        new_valid_prefixes = []
        for combination in generate_combinations('', length, valid_prefixes):
            url = f"{base_url}{combination}"
            if check_url(url):
                write_valid_url(url)  # 更新last_valid_url变量
                new_valid_prefixes.append(combination)
        valid_prefixes = new_valid_prefixes
except Exception as e:
    print(f"Error: {e}")
finally:
    # 取消定时器
    signal.alarm(0)

    # 将临时文件的内容追加到start_point.config文件中
    with open(temp_file, 'r') as file:
        with open(start_point_config, 'a') as file:
            file.writelines(file)

    # 清理临时文件
    os.remove(temp_file)
