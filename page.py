from selenium import webdriver
import time
import os.path
from selenium.webdriver.chrome.options import Options
from hoshino import R, Service, priv, util

sv = Service('网页截图')

def getpic(url,saveImgName):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    chromedriver = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(options=options,executable_path =chromedriver)
    driver.maximize_window()
    js_height = "return document.body.clientHeight"
    picname = saveImgName
    link = url 
    try:
        driver.get(link)
        k = 1
        height = driver.execute_script(js_height)
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                print(js_move)
                driver.execute_script(js_move)
                time.sleep(0.2)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(picname + ".png")
        return True
    except Exception as e:
        return False
       
 
@sv.on_prefix('截图')
async def pic(bot, event):
    path = ev.message.extract_plain_text().split()
    if 'http://' not in path and 'https://' not in path:
        path='http://'+path
    ss=getpic(path,'C:\\nb2\\mimibot\\src\\plugins\\pcr-rank\\img\\imgs')
    if ss==True:
        await bot.send(event,R.img('imgs.png').cqcode)
    else:
        await bot.send(event,'获取失败，呜呜呜，可能是因为地址错误或链接超时')
