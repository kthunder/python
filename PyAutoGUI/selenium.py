from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pprint import pprint

# 无界面的浏览器
if 2==1:
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(options=option)
else:
    browser = webdriver.Chrome()

# 截图预览
# browser.get_screenshot_as_file('截图.png')

# 设置浏览器大小：全屏
browser.maximize_window()
browser.get(r'http://192.168.2.7/polarion/#/project/Alioth8_Sw/wiki/MCAL/TTAS_FM724_MCAL_SST_FLS_EEP')

browser.find_element(By.ID, "j_username").send_keys('wujialin')

browser.find_element(By.ID, "j_password").send_keys('123456')

browser.find_element(By.ID, "submitButton").click()

time.sleep(5)

iframe = browser.find_element(By.ID, 'gwt-debug-polarion-DLE-area-debug-id')
print("iframe", iframe)
browser.switch_to.frame(iframe)
items = browser.find_elements(By.ID, 'polarion_wiki macro name=module-workitem;params=id=A8S-3937')
for item in items:
    print("item", item)

# 回车查询
# input.submit()
time.sleep(10)

browser.close()

