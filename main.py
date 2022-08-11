import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
import re
import json
import os
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    # 'referer': 'https://www.douyin.com/'
}


def parse_url(url):
    url = re.findall('[a-zA-z0-9]+:\/\/[^\s]*', url)
    if len(url) == 0:
        log.insert(END, f'输入错误! \n')
        return 
    if 'douyin.com' in url[0]:
        log.insert(END, f'抖音 \n')
        douyin(url[0])
    else:
        log.insert(END, f'不支持该链接! \n')


def fixname(author, create_time, desc, isDir=False, limit=200):
    local_str_time = datetime.fromtimestamp(
        create_time).strftime('%Y-%m-%d %H-%M-%S')
    filename = f'{local_str_time} {desc}'
    character = r'[\n\r\t?*/\\|:><"]'
    # 用正则表达式去除windows下的特殊字符，这些字符不能用在文件名
    filename = re.sub(character, "", filename)
    if len(filename) > limit:  # 防止文件名过长,linux 和 windows 文件名限制约为 255 个字符
        filename = filename[:int(limit / 2) - 3] + '...' + \
            filename[len(filename) - int(limit / 2):]
    if author != '':
        author_path = f'{os.getcwd()}/download/{author}'
        if not os.path.exists(author_path):
            os.mkdir(author_path)
        filename = f'{os.getcwd()}/download/{author}/{filename}'
    else:
        filename = f'{os.getcwd()}/download/{filename}'
    if isDir:
        if not os.path.exists(filename):
            os.mkdir(filename)
        else:
            print()
            log.insert(END, f'已下载! {filename} \n')
            return False
    else:
        if os.path.exists(f'{filename}.mp4'):
            log.insert(END, f'已下载! {filename} \n')
            return False
    return filename


def douyin(url):
    if re.findall('/video/(\d+)?', url):
        __douyin_one(re.findall('/video/(\d+)?', url)[0])
    elif re.findall('modal_id=(\d+)', url):
        __douyin_one(re.findall('modal_id=(\d+)', url)[0])
    elif re.findall('/note/(\d+)', url):
        __douyin_one(re.findall('/note/(\d+)', url)[0])
    elif re.findall('douyin.com/user/(.*)', url):
        __douyin_all(re.findall('douyin.com/user/(.*)', url)[0])
    else:
        log.insert(END, f'解析链接错误! \n')


def __douyin_one(key, author=''):
    src_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={key}'
    response_src = requests.get(url=src_url, headers=headers).json()

    if response_src["item_list"][0]["images"] is None:
        filename = fixname(
            author, response_src["item_list"][0]["create_time"], response_src["item_list"][0]["desc"])
        if filename == False:
            return
        log.insert(END, f'下载视频...... {filename} \n')
        video_url = response_src["item_list"][0]["video"]["play_addr"]["url_list"][0]
        video_url_rmwm = video_url.replace("playwm", "play", 1)

        video_src = requests.get(url=video_url_rmwm, headers=headers).content
        with open(f'{filename}.mp4', 'wb') as f:
            f.write(video_src)
        log.insert(END, f'===完成 \n')
    else:
        filename = fixname(
            author, response_src["item_list"][0]["create_time"], response_src["item_list"][0]["desc"], True)
        if filename == False:
            return
        log.insert(END, f'下载图集...... {filename} \n')
        list_url = []  # 图片的url列表
        list_src = response_src["item_list"][0]["images"]
        for i in list_src:
            url_l = i['url_list'][3]
            list_url.append(url_l)
        count = 0

        for i in list_url:
            images_response = requests.get(
                url=i, headers=headers).content
            with open(f'{filename}/{count}.jpeg', 'wb+') as f:
                f.write(images_response)
            count = count + 1
        log.insert(END, f'===完成 \n')

def __douyin_all(sec_uid):
    max_cursor = 0
    keys = []
    author = ''
    while 1:
        pageurl = f'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={sec_uid}&count=15&max_cursor={max_cursor}'
        listpage = requests.get(url=pageurl, headers=headers).text
        listpage = json.loads(listpage)
        if max_cursor == 0:
            author = listpage['aweme_list'][0]['author']['nickname']
        max_cursor = listpage["max_cursor"]
        for aweme in listpage['aweme_list']:
            keys.append(aweme['aweme_id'])
        if max_cursor == 0:
            break
    total = len(keys)
    log.insert(END, f'{author} 共解析到 {total} 条记录 \n')
    for key in keys:
        __douyin_one(key, author)


if __name__ == '__main__':
    root = ttk.Window(
        title="Dr Crawls",
        minsize=(800, 600)
    )
    app = ttk.Frame(root, padding=15)
    app.pack(fill=BOTH, expand=YES)

    bar = ttk.Frame(app)
    bar.pack(fill=X, pady=1, side=TOP)

    text = ttk.Text(bar, height=2)
    text.pack(side=LEFT, fill=X, expand=YES, padx=(0, 5), pady=10)

    btn = ttk.Button(bar, text="Dowmload",
                     command=lambda: parse_url(text.get('0.0', 'end')))
    btn.pack(side=LEFT, fill=X, padx=(5, 0), pady=10)

    log = ttk.ScrolledText(app)
    log.pack(fill=BOTH, expand=YES)
    default_txt = f'请输入您要爬取的链接\n'
    log.insert(END, default_txt)

    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    dialog_width = 800
    dialog_height = 600
    root.geometry("%dx%d+%d+%d" % (dialog_width, dialog_height,
                  (screenwidth-dialog_width)/2, (screenheight-dialog_height)/2))
    root.mainloop()
