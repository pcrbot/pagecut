from selenium import webdriver
import time
from hoshino import R, Service, config, get_bot
import os
import json

# from webdriver_manager.chrome import ChromeDriverManager

sv = Service(
    name='网页截图',
    visible=False,
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐'
)

group_list = []
FILE_PATH = os.path.dirname(__file__)


def save_group_list():
    with open(os.path.join(FILE_PATH, 'group_list.json'), 'w', encoding='UTF-8') as f1:
        json.dump(group_list, f1, ensure_ascii=False)


# 检查group_list.json是否存在，没有创建空的
if not os.path.exists(os.path.join(FILE_PATH, 'group_list.json')):
    save_group_list()

# 读取group_list.json的信息
with open(os.path.join(FILE_PATH, 'group_list.json'), 'r', encoding='UTF-8') as f:
    group_list = json.load(f)


def getpic(url, save_img_name, _type):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    chromedriver = config.RES_DIR + "chromedriver"
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, executable_path=chromedriver)
    driver.maximize_window()
    js_height = "return document.body.clientHeight"
    picname = save_img_name
    link = url
    try:
        # print(link)
        driver.get(link)
        k = 1
        height = driver.execute_script(js_height)
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                # print(js_move)
                driver.execute_script(js_move)
                time.sleep(0.2)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        if not _type == "":
            scroll_width = 600
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(picname + ".png")
        return True
    except Exception as e:
        print(e)
        return False


def get_src_code(url, type_="src", js_var=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    chromedriver = config.RES_DIR + "chromedriver"
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, executable_path=chromedriver)
    driver.maximize_window()
    link = url
    try:
        driver.get(link)
        if type_ == "src":
            return driver.page_source
        elif type_ == "jsvar" and js_var is not None:
            return driver.execute_script(f"return {js_var}")
    except Exception as e:
        print(e)
        return False


@sv.on_prefix(["获取网页源代码", "getsrccode"])
async def qq_get_src(bot, ev):
    var = ev.message.extract_plain_text().split()
    if not len(var) > 1:
        await bot.finish(ev, "参数错误")
    url = var[0]
    type_ = var[1]
    if type_ == "jsvar":
        if not len(var) > 2:
            await bot.finish(ev, "参数错误")
    js_var = var[2]
    src_code = get_src_code(url, type_, js_var)
    path = os.path.join(os.path.dirname(__file__), "data.txt")
    with open(path, "w", encoding="utf-8") as file:
        if isinstance(src_code, list) or isinstance(src_code, dict):
            file.write(json.dumps(src_code, indent=2, ensure_ascii=False))
        if isinstance(src_code, str):
            file.write(src_code)
    await bot.finish(ev, "完成")


@sv.on_prefix('网页截图')
async def pic(bot, ev):
    var = ev.message.extract_plain_text().split()
    path = var[0]
    # noinspection HttpUrlsUsage
    if 'http://' not in path and 'https://' not in path:
        # noinspection HttpUrlsUsage
        path = 'http://' + path
    ss = getpic(path, config.RES_DIR + "img/screenshot", "")
    if ss:
        await bot.send(ev, R.img('screenshot.png').cqcode)
    else:
        await bot.send(ev, '获取失败，呜呜呜，可能是因为地址错误或链接超时')
