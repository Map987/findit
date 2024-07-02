import requests
import urllib3

# 禁用警告
urllib3.disable_warnings()

# 基础URL和输出文件
base_url = 'https://esercenti.luckyred.it/film/'
output_file = 'valid_urls.txt'  # 输出文件名
max_length = 20  # 设置最大组合长度

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

# 初始化有效前缀列表
valid_prefixes = [start_point]

# 生成所有可能的字母组合
for length in range(len(start_point), max_length + 1):
    new_valid_prefixes = []
    for combination in generate_combinations('', length, valid_prefixes):
        url = f"{base_url}{combination}"
        if check_url(url):
            write_valid_url(url)
            new_valid_prefixes.append(combination)
    valid_prefixes = new_valid_prefixes
