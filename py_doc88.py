from selenium import webdriver
import os
import time

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from lxml import etree

chromeOptions = webdriver.ChromeOptions()
# browser=webdriver.Chrome(executable_path=r"C:\sources\chromedriver_win32\chromedriver.exe")
path = os.getcwd() + '\data'
options = Options()
# 判断文件夹是否存在，不存在创建文件夹
is_exists = os.path.exists(path)
if not is_exists:
    os.mkdir(path)

# 指定浏览器下载文件夹 #"download.default_directory": path 下载文件存的路径，，，
# "profile.default_content_setting_values.automatic_downloads":1设置下载多个文件，免得弹出框在下载过程中出现    牛牛牛
prefs = {"download.default_directory": path, "profile.default_content_setting_values.automatic_downloads": 1}
options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(chrome_options=options, executable_path=r"C:\sources\chromedriver_win32\chromedriver.exe")
# 指定网页链接


url = 'https://www.doc88.com/p-549550988532.html'
# browser.get('https://www.doc88.com/p-5969904068700.html')  #论文
browser.get(url)
# 网页源代码

text = browser.page_source
html = etree.HTML(text)
page_num = html.xpath("//li[@class='text']/text()")[0]
# 获取总页码数
page_num = int(page_num.replace('/ ', ''))
print(f'共{page_num}页')
print(EC.visibility_of_element_located((By.XPATH, "//div[@id='continueButton']")))
# #等待网页加载
time.sleep(10)
# 等待按钮
element = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='continueButton']")))
element.click()

# browser.find_element_by_xpath("//div[@id='continueButton']").click()


js = "return action=document.body.scrollHeight"
# 初始化现在滚动条所在高度为0
height = 0
# 当前窗口总高度
new_height = browser.execute_script(js)
k = 0

while k <= page_num:
    for i in range(height, new_height, 3000):
        k += 1
        browser.execute_script('window.scrollTo(0, {})'.format(i))
        time.sleep(1)
        a = f"downloadPages({k}, {k})"
        # 中间需要手动点一下运行下载多个文件
        browser.execute_script("""function downloadPages(from, to) {
            for (i = from; i <= to; i++) {
                const pageCanvas = document.getElementById('page_' + i);
                if (pageCanvas === null) break;
                pageNo_ = i >= 10 ? ''+i:'0'+i;
                const pageNo = pageNo_;
                pageCanvas.toBlob(
                    blob => {
                        const anchor = document.createElement('a');
                        anchor.download = 'page_' + pageNo + '.png';
                        anchor.href = URL.createObjectURL(blob);
                        anchor.click();
                        URL.revokeObjectURL(anchor.href);
                    }
                    //, 'image/jpeg' // (*)
                    //, 0.9          // (*)
                );
            }
        };
        """ + a)
        # try:
        #     if EC.alert_is_present():
        #         print("1111")
        #         browser.switch_to.alert.accept()
        # except NoAlertPresentException:
        #     continue
