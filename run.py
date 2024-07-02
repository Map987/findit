import requests
import certifi
import urllib3
import requests
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

cookie = [
    {
        "name": cookie_name,
        "value": cookie_value  # 假设值确实是空的
    },
    {
        "name": "wordpress_test_cookie",
        "value": "WP+Cookie+check"
    }
]

# 构建Cookie头
cookie_header = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookie])

# 如果有多个cookie，可以按如下方式添加
# cookie_header = "name1=value1; name2=value2; name3=value3"

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
  #  print(film_page_soup)
    dropbox_links_on_page = film_page_soup.find_all('a', href=True)
    print(dropbox_links_on_page)

    dropbox_links = [link['href'] for link in dropbox_links_on_page if link['href'].startswith('https://www.dropbox.com/')]
    # 将Film URL和对应的Dropbox链接添加到字典中
    film_urls_with_dropbox[film_url] = dropbox_links

with open('dropbox_links.json', 'w') as json_file:
    json.dump(film_urls_with_dropbox, json_file, indent=4)
