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
#args = parser.parse_args()

# 从命令行参数中获取cookie的name和value
#cookie_name = args.account
#cookie_value = args.password

#cookie = {
   # "name": cookie_name,
   # "value": cookie_value  # 假设值确实是空的
#}

# 构建Cookie头
#cookie_header = "; ".join(f"{c['name']}={c['value']}" for c in [cookie, {"name": "wordpress_test_cookie", "value": "WP+Cookie+check"}])
import requests
import re
import json

# 设置登录页面的URL
url = 'https://esercenti.luckyred.it/account'

# 发送GET请求获取页面源码
response = requests.get(url, verify=False)
ok = response.text
cookie_name = 'wordpress_test_cookie'
cookie_value = 'WP+Cookie+check'
# 检查请求是否成功
if response.status_code == 200:
    # 使用正则表达式提取ur_login_form_save_nonce的值
    nonce_pattern = r'var ur_login_params = ({.*?});'
    matches = re.search(nonce_pattern, response.text)
    print(matches)
    if matches:
        # 解析匹配到的JSON字符串
        ur_login_params = json.loads(matches.group(1))
        security_nonce = ur_login_params.get('ur_login_form_save_nonce', '')
        print(f"Security nonce: {security_nonce}")
        
        # 现在使用提取到的security_nonce进行登录
        login_url = 'https://esercenti.luckyred.it/wp-admin/admin-ajax.php'
        login_data = {
            'action': 'user_registration_ajax_login_submit',
            'security': security_nonce,
            'username': 'categorydev',  # 替换为您的用户名
            'password': 'Jabgau.465',  # 替换为您的密码
            'rememberme': 'forever',
            'redirect': '%2F'
        }
        
        # 发送POST请求进行登录
        login_response = requests.post(login_url, data=login_data, verify=False)
        
        # 检查登录响应
        if login_response.status_code == 200:
            print("登录成功")
            # 打印响应内容
            print(login_response.text)
        else:
            print(f"登录失败，状态码：{login_response.status_code}")
    else:
        print("未能找到ur_login_form_save_nonce的值")
else:
    print(f"请求失败，状态码：{response.status_code}")
cookies = login_response.cookies
print(cookies)
cookie_header = "; ".join(f"{cookie.name}={cookie.value}" for cookie in cookies)
print(cookie_header)
cookie_header += f"; {cookie_name}={cookie_value}"
print(cookie_header)

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
    print(dropbox_links)

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
