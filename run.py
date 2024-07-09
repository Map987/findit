import requests
import certifi
import urllib3
from bs4 import BeautifulSoup
import json
import os
import sys
import argparse

urllib3.disable_warnings()

parser = argparse.ArgumentParser(description='Process some integers.')
# 添加参数
parser.add_argument('--account', type=str, help='Cookie name')
parser.add_argument('--password', type=str, help='Cookie value')

# 解析参数
args = parser.parse_args()

# 从命令行参数中获取cookie的name和value
cookie_name = args.account
cookie_value = args.password

cookie = {
    "name": cookie_name,
    "value": cookie_value  # 假设值确实是空的
}

# 构建Cookie头
cookie_header = "; ".join(f"{c['name']}={c['value']}" for c in [cookie, {"name": "wordpress_test_cookie", "value": "WP+Cookie+check"}])

# 设置请求头
headers = {
    'Cookie': cookie_header,
    # 其他可能需要的请求头
}

# 发送请求
response = requests.get('https://esercenti.luckyred.it', headers=headers, verify=False)

films_soup = BeautifulSoup(response.text, 'html.parser')
film_links = films_soup.find_all('a', href=True)
film_urls = [link['href'] for link in film_links if link['href'].startswith('https://esercenti.luckyred.it/film/')]

film_urls_with_dropbox = {}

for film_url in film_urls:
    film_page_response = requests.get(film_url, headers=headers, verify=False)
    film_page_soup = BeautifulSoup(film_page_response.text, 'html.parser')
    dropbox_links_on_page = film_page_soup.find_all('a', href=True)
    dropbox_links = [link['href'] for link in dropbox_links_on_page if link['href'].startswith('https://www.dropbox.com/')]

    # 检查 film_url 是否已存在于字典中
    if film_url in film_urls_with_dropbox:
        # 如果存在，则将新的 dropbox_links 追加到现有列表中
        film_urls_with_dropbox[film_url].extend(dropbox_links)
    else:
        # 如果不存在，则创建一个新的条目
        film_urls_with_dropbox[film_url] = dropbox_links

# 保存到 JSON 文件
with open('dropbox_links.json', 'w') as json_file:
    json.dump(film_urls_with_dropbox, json_file, indent=4)
