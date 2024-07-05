import requests
import urllib3
import signal
import time

# 禁用警告
urllib3.disable_warnings()

# 基础URL和输出文件
base_url = 'https://esercenti.luckyred.it/film/'
output_file = 'valid_urls.txt'  # 输出文件名
max_length = 20  # 设置最大组合长度
max_execution_time = 5 * 3600  # 4小时转换为秒

# 读取已存在的有效URL
def read_valid_prefixes(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.strip().split('/')[-1] for line in file]
    except FileNotFoundError:
        return []

# 读取文件中的最后一行前缀
def read_last_line_prefix(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[-1].strip().split('/')[-1]
            else:
                return ''
    except FileNotFoundError:
        return ''

# 检查URL
def check_url(url):
    response = requests.get(url, verify=False)
    return response.status_code == 200

# 写入有效的URL
def write_valid_url(url):
    with open(output_file, 'a') as file:
        file.write(url + '\n')
    print(f"Found valid URL: {url}")

# 超时处理
def timeout_handler(signum, frame):
    raise Exception("Execution time limit reached")

# 设置定时器
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(max_execution_time)

try:
    # 从文件中读取已存在的有效前缀
    valid_prefixes = read_valid_prefixes(output_file)

    # 如果文件不存在或为空，则从空字符串开始生成组合
    if not valid_prefixes:
        valid_prefixes = ['']
    else:
        # 找到最长的有效前缀
        last_prefix = max(valid_prefixes, key=len)
        # 使用长度减1的有效前缀作为基础
        valid_prefixes = [prefix for prefix in valid_prefixes if len(prefix) == len(last_prefix) - 1]

    # 读取文件中的最后一行前缀
    last_line_prefix = read_last_line_prefix(output_file)

    # 继续生成新的组合
    for length in range(1, max_length + 1):
        new_valid_prefixes = []
        for prefix in valid_prefixes:
            for char in '-abcdefghijklmnopqrstuvwxyz':
                new_prefix = prefix + char
                # 只有当新的前缀大于文件中末尾的前缀值时才进行检查
                if new_prefix > last_line_prefix:
                    url = f"{base_url}{new_prefix}"
                    if check_url(url):
                        write_valid_url(url)
                        new_valid_prefixes.append(new_prefix)  # 将新的有效前缀添加到列表中
        valid_prefixes = new_valid_prefixes  # 更新有效前缀列表

except Exception as e:
    print(f"Error: {e}")
finally:
    # 取消定时器
    signal.alarm(0)
