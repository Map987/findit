import requests
import urllib3
import signal
import time

# 禁用警告
urllib3.disable_warnings()

# 基础URL和输出文件
base_url = 'https://esercenti.luckyred.it/films/'
output_file = '/content/valid_urls.txt'  # 输出文件名
max_length = 2  # 设置最大组合长度
max_execution_time = 5 * 3600  # 5小时转换为秒

# 用户指定的开始点
start_point = 'bl'

def generate_combinations(prefix, length, start_combination, start_length):
    if len(prefix) >= start_length and prefix < start_combination:
        return []
    if length == 0:
        return [prefix] if len(prefix) >= start_length else []
    combinations = []
    for char in '-abcdefghijklmnopqrstuvwxyz':
        new_prefix = prefix + char
        combinations.extend(generate_combinations(new_prefix, length - 1, start_combination, start_length))
    return combinations

def check_url(url):
    response = requests.get(url, verify=False)
    return response.status_code == 200

def write_valid_url(url):
    with open(output_file, 'a') as file:
        file.write(url + '\n')
    print(f"Found valid URL: {url}")

def timeout_handler(signum, frame):
    raise Exception("Execution time limit reached")

# 设置定时器
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(max_execution_time)

try:
    # 生成所有可能的字母组合
    for length in range(1, max_length + 1):
        for combination in generate_combinations('', length, start_point, len(start_point)):
            url = f"{base_url}{combination}"
            if check_url(url):
                write_valid_url(url)
except Exception as e:
    print(f"Error: {e}")
finally:
    # 取消定时器
    signal.alarm(0)
