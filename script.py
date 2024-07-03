import requests
import urllib3
import signal
import time

# 禁用警告
urllib3.disable_warnings()

# 基础URL和输出文件
base_url = 'https://esercenti.luckyred.it/films/'
output_file = 'valid_urls.txt'  # 输出文件名
max_length = 20  # 设置最大组合长度
max_execution_time = 5 * 3600  # 设置最大执行时间为5分钟（例如）

# 用户指定的开始点
start_point = 'b---'

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

def load_valid_prefixes(length):
    valid_prefixes = set()
    with open(output_file, 'r') as file:
        for line in file:
            url = line.strip()
            if len(url) == length:
                valid_prefixes.add(url[:-1])  # 移除最后一个字符以获取前缀
    return list(valid_prefixes)

def update_start_point(new_prefix):
    with open('start_point.config', 'w') as file:
        file.write(new_prefix)

def timeout_handler(signum, frame):
    raise Exception("Execution time limit reached")

# 设置定时器
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(max_execution_time)

# Initialize new_valid_prefixes outside the try block
new_valid_prefixes = []  

try:
    # 初始化有效前缀列表
    valid_prefixes = load_valid_prefixes(max_length - 1)

    # 如果有效前缀列表为空，则使用start_point
    if not valid_prefixes:
        valid_prefixes = [start_point]

    # 生成所有可能的字母组合
    for length in range(len(start_point), max_length + 1):
        # new_valid_prefixes = []  # Move this inside the loop to reset for each length
        for combination in generate_combinations('', length, valid_prefixes):
            url = f"{base_url}{combination}"
            if check_url(url):
                write_valid_url(url)
                new_valid_prefixes.append(combination)
                update_start_point(combination)  # 更新start_point
        valid_prefixes = new_valid_prefixes # Update valid_prefixes after each length
except Exception as e:
    print(f"Error: {e}")
finally:
    # 取消定时器
    signal.alarm(0)
    # 如果找到了有效的URL，则将其写入配置文件
    if new_valid_prefixes:
        update_start_point(new_valid_prefixes[-1])

# 在finally块之后，我们可以安全地访问new_valid_prefixes
if new_valid_prefixes:
    print(f"Updated start_point to {new_valid_prefixes[-1]}")
