#取得關注者列表
import requests
import re
import http.cookiejar
from bs4 import BeautifulSoup
session = requests.session()

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
session.headers = headers
session.cookies = http.cookiejar.LWPCookieJar(filename='cookies')

params = {
    'lang': 'zh_tw',
    'source': 'pc',
    'view_type': 'page',
    'ref': 'wwwtop_accounts_index'
}
session.cookies.load(filename='cookies', ignore_discard=True)
url = 'https://www.pixiv.net/bookmark.php?type=user'
# 获取登录页面
res = session.get(url)
# 获取post_key


teamp = res.content
teamp = res.text
teamp = ''.join(teamp)

# 編譯成 Pattern 對象
pattern = re.compile('value="([0-9]+)"')
# 取得匹配結果，無法匹配返回 None
match = pattern.findall(teamp)






fo = open("html.txt", "w",encoding="utf-8")
fo.write( teamp)
fo.close()


fo = open("userID.txt", "w",encoding="utf-8")
fo.write("\n".join(match))
fo.close()




