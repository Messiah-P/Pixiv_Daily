import time
import requests
import re
import datetime
import traversal
import os
import concurrent.futures
import socket
from fake_useragent import UserAgent
from extract import extract_pic_info
from pathlib import Path
from log import log_output

PIXIV_DIR = '/mnt/photo/Pixiv'
ALL_PATHS = ['/mnt/photo/Pixiv', '/mnt/photo/画师']
LOGO_PIXIV = 'https://lsky.pantheon.center/image/2022/11/20/637a374fa4aca.jpeg'
HEAD_BARK = 'https://bark.pantheon.center/WSeN8LCGbCDZqHAJMTmeHP'

repeat = 1
time_now = datetime.datetime.now()
time_yesterday = time_now + datetime.timedelta(days=-1)
log_path = f"/mnt/nfs/Config/Log/Pixiv/{datetime.datetime.now():%Y-%m-%d}.log"

headers = {
    'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
    'user-agent': UserAgent(verify_ssl=False).random,
    'Cookie': open('/mnt/python/Pixiv/cookie.txt', 'r').read().strip()
}

def get_single_pic(url, count):
    global repeat
    retry = 1
    while True:
        try:
            # 使用Session对象，提升请求效率
            with requests.Session() as session:
                response = session.get(url, headers=headers, timeout=(3, 17))
                name, user_name, picture, pid = extract_pic_info(response.text)
                name = re.sub(r'[\\/:\*\?"<>\|]', str(repeat), name)
                repeat += 1
                user_name = re.sub(r'[\\/:\*\?"<>\|]', str(repeat), user_name)
                repeat += 1
                pic = requests.get(picture, headers=headers)
                pic_name = f"{count} - {user_name} - {name}[pid={pid}].{picture[-3:]}"
                log_output(f"图名={pic_name}")
                break
        except (requests.exceptions.RequestException, socket.timeout):
            log_output(f"第{count}张图片下载失败，正在进行第{retry}次重试...")
            time.sleep(3)
            retry += 1
            if retry > 5:
                log_output(f"第{count}张图片下载失败，重试次数过多，已跳过。")
                return count, False
    # 创建文件夹路径下载
    path = Path(PIXIV_DIR) / str(time_yesterday.year) / str(time_yesterday.month) / f'{str(time_yesterday.day)}_daily'
    os.makedirs(path, mode=0o777, exist_ok=True)
    path = f'{path}/{pic_name}'
    with open(path, 'wb') as f:
        f.write(pic.content)
    os.chmod(path, mode=0o777)
    return count, True

def print_result(future):
    count, result = future.result()
    if result:
        log_output(f"第{count}张图片下载成功！")
    else:
        log_output(f"第{count}张图片下载失败！")

def get_all_pic_url():
    count = 1
    valid_count = 0
    invalid_count = 0
    traversal_list = traversal.all_pids(ALL_PATHS)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for n in range(1, 10 + 1):
            # 使用f-string格式化字符串，更加简洁明了
            url = f'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p={n}&format=json'
            # 使用Session对象，提升请求效率
            with requests.Session() as session:
                response = session.get(url, headers=headers)
                illust_id = re.findall('"illust_id":(\d+?),', response.text)
                picUrl = ['https://www.pixiv.net/artworks/' + i for i in illust_id]
            futures = []
            for url in picUrl:
                if count <= 50:
                    pid = url.split('/')[4]
                    if pid not in traversal_list:
                        log_output(f"正在下载第{count}张图片")
                        # 使用线程池并发下载
                        future = executor.submit(get_single_pic, url, count)
                        future.add_done_callback(print_result)
                        count += 1
                        valid_count += 1
                    else:
                        log_output(f"第{count}张图片(pid={pid}),重复跳过!")
                        count += 1
                        invalid_count += 1
                else:
                    break
            concurrent.futures.wait(futures)
    with requests.Session() as ret:
        bark = ret.get('%s/Pixiv日榜更新/成功获取新图：%d张\n重复：%d张?icon=%s&group=Pixiv'% (HEAD_BARK,valid_count,invalid_count,LOGO_PIXIV))
    return None

if __name__ == '__main__':
    get_all_pic_url()