from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(executable_path=r'C:\Users\shiro\PycharmProjects\untitled3\chromedriver_win32\chromedriver.exe',chrome_options=chrome_options)  # PhantomJs
driver.get('http://pala.tw/js-example/')  # 輸入範例網址，交給瀏覽器 
pageSource = driver.page_source  # 取得網頁原始碼
print(pageSource)



driver.close()
#illust_id=