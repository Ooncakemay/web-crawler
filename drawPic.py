#抓取使用者作品圖片
from selenium import webdriver
import requests
import re
import http.cookiejar
from bs4 import BeautifulSoup
import os
import math

def reFullWorkPage(session,id):
    # 作者id引索值
    params = {
        'id': id,
    }

    url = 'https://www.pixiv.net/member_illust.php?id='+id
    # 取的作者作品頁面
    res = session.get(url, params=params)
    # 將網頁整合成單一string
    fist_page = res.text
    fist_page = ''.join(fist_page)

    # 有幾頁作品
    work_quantity_patten = '<span class="count-badge">([0-9]+)件</span>'
    pattern = re.compile(work_quantity_patten)
    number = pattern.findall(fist_page)
    page = int(math.ceil(float(number[0]) / 20))

    #https://www.pixiv.net/member_illust.php?id=43070&type=all&p=4
    web_pag = [fist_page]
    for web_num in range(2,page+1):
        url = 'https://www.pixiv.net/member_illust.php?id='+id+'&type=all&p=' + str(web_num)
        params = {
            'id': id,
            'type':'all',
            'p':str(web_num)
        }
        res = session.get(url, params=params)
        tamp= res.text
        web_pag.append(''.join(tamp))
    return web_pag

def saveWorkImage(work_id, work_data, individual_work_quantity, session, folder_path,style,work_file):

    web_path = 'https://i.pximg.net/img-original/img/'
    head_path_manga = 'https://www.pixiv.net/member_illust.php?mode=manga_big&illust_id='
    head_path_medium = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='
    #referer:https://www.pixiv.net/member_illust.php?mode=medium&illust_id=48150885
    # referer:https://www.pixiv.net/member_illust.php?mode=manga_big&illust_id=62997530&page=0


    folder_path = folder_path + work_id + '/'
    if os.path.exists(folder_path) == False:
        os.makedirs(folder_path)

    for i in range(0, int(individual_work_quantity)):
        # 標頭設定
        path = web_path + work_data + work_id + '_p' + str(i) + work_file
        if style == 'manga':
            head_path_img = head_path_manga + work_id + '&page=' + str(i)
        else:
            head_path_img = head_path_medium + work_id
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Referer': head_path_img
        }
        session.headers = headers


        html = session.get(path)
        if html.status_code != 200:
            work_file = '.png'
            path = web_path + work_data + work_id + '_p' + str(i) + work_file
            html = session.get(path)



        # 貯存圖片
        img_name = folder_path + str(i + 1) + work_file
        with open(img_name, 'wb') as file:
            file.write(html.content)
            file.flush()
        file.close()
        print('第%d張圖片下载完成' % (i + 1))
    print('抓取完成')




#========================= 開始 ======================================
session = requests.session()
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
#Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36
session.headers = headers
session.cookies = http.cookiejar.LWPCookieJar(filename='cookies')
session.cookies.load(filename='cookies', ignore_discard=True)

#取得作者作品頁面
id = '3137712'
fullPage = reFullWorkPage(session,id)
#匹配、抓取作品資料
work_id_list = []
work_count = {}
work_data = []
work_file = []

# 取得作品id
pattern_id = re.compile('illust_id=([0-9]+)"class')
# 個別作品的張數
#找出標簽
pattern_work_page_count= re.compile('<span>[0-9]+</span></div></a><a href=".+?mode=medium&amp;illust_id=[0-9]+')
#找出標籤裡的id
pattern_span_id = re.compile("illust_id=([0-9]+)")
#找出count 數量
patten_work_span = re.compile( '<span>([0-9]+)</span>')
#作品上傳日期
pattern_data = re.compile('img-master/img/([0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+/[0-9]+/)')
#作品格式 master[0-9]+(.[a-z]+)"
pattern_file = re.compile('master[0-9]+(.[a-z]+)"')


for item in fullPage:
    math = pattern_id.findall(item)
    work_id_list.extend(math)
    #包含作品id 跟 數量的片段
    math = pattern_work_page_count.findall(item)
    for span in math:
        count = patten_work_span.findall(span)
        work_id_for_span = pattern_span_id.findall(span)
        work_count[work_id_for_span[0]] = int(count[0])
    math = pattern_data.findall(item)
    work_data.extend(math)
    math = pattern_file.findall(item)
    work_file.extend(math)


#寫檔
fo = open("work_list.txt", "w",encoding="utf-8")
fo.write("\n".join(work_id_list))
fo.close()

fo = open("individual_work_quantity.txt", "w",encoding="utf-8")
fo.write("\n".join(work_count))
fo.close()

fo = open("work_data.txt", "w",encoding="utf-8")
fo.write("\n".join(work_data))
fo.close()

fo = open("work_file.txt", "w",encoding="utf-8")
fo.write("\n".join(work_file))
fo.close()



folder_path = './photo'+id+'/'
print(type(folder_path))
if os.path.exists(folder_path) == False:  # 判斷文件夾是否存在
    os.makedirs(folder_path)  # 建立文件夾



#key in d
for index, work in enumerate(work_id_list):
    if work in work_count:
        saveWorkImage(work, work_data[index], work_count[work], session, folder_path, style = "manga",work_file=work_file[index])
    else:
        saveWorkImage(work,work_data[index],1,session,folder_path,style='medium',work_file=work_file[index])












