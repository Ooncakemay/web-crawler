#下載img
#<span class="total">

import requests
import shutil
import re
import http.cookiejar
import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time

session = requests.session()


params = {
    'mode': 'manga',
    'illust_id': '28118586'
}
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
session.headers = headers
session.cookies = http.cookiejar.LWPCookieJar(filename='cookies')
session.cookies.load(filename='cookies', ignore_discard=True)
url = 'https://www.pixiv.net/member_illust.php?mode=manga&illust_id=28118586'

# 获取登录页面
res = session.get(url)

teamp = res.content
teamp = res.text
teamp = ''.join(teamp)


# 編譯成 Pattern 對象
pattern = re.compile('illust_id=([0-9]+)"class')
# 取得匹配結果，無法匹配返回 None
match = pattern.findall(teamp)


soup = BeautifulSoup(res.content, 'html.parser')
items = soup.find_all('img')
folder_path = './photo/'
if os.path.exists(folder_path) == False:  # 判断文件夹是否已经存在
    os.makedirs(folder_path)  # 创建文件夹

for index, item in enumerate(items):
    if item:
        print(item.get('src'))
        html = session.get(item.get('src'))  # get函数获取图片链接地址，requests发送访问请求
        img_name = folder_path + str(index + 1) + '.jpg'
        with open(img_name, 'wb') as file:  # 以byte形式将图片数据写入
            file.write(html.content)
            file.flush()
        file.close()  # 关闭文件
        print('第%d张图片下载完成' % (index + 1))
        time.sleep(1)  # 自定义延时
print('抓取完成')



