import os
import time
import socket
import requests
import concurrent.futures
from pathlib import Path
from extract import extract_pic_info
from log import log_output
from conf.config import PIXIV_DIR, ALL_PATHS, LOGO_PIXIV, HEAD_BARK, time_yesterday
from preprocess import headers, get_all_pic_url
from traversal import all_pids,update_all_artworks
from db.artworks import query

repeat = 1

def get_single_pic(url, count):
    global repeat
    retry = 1
    while True:
        log_output(f"正在处理第{count}张图片...")
        try:
            # 使用Session对象，提升请求效率
            with requests.Session() as session:
                response = session.get(url, headers=headers, timeout=(3, 17))
                name, user_name, picture, pid, repeat = extract_pic_info(response.text, repeat)
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

def multithread_download(picUrl):
    retry = 1
    count = 1
    valid_count = 0
    invalid_count = 0
    while True:
        try:
            log_output(f"开始创建多线程下载...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for url in picUrl:
                    if count <= 50:
                        pid = url.split('/')[4]
                        #if pid not in traversal_list:
                        if query("artworks", pid):
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
                log_output(f"正在等待下载完成...")
                concurrent.futures.wait(futures)
            log_output(f"获取新图{valid_count}张,重复{invalid_count}张,下载完成！")
            with requests.Session() as ret:
                bark = ret.get('%s/Pixiv日榜更新/成功获取新图：%d张\n重复：%d张?icon=%s&group=Pixiv' % (HEAD_BARK, valid_count, invalid_count, LOGO_PIXIV))
            break
        except (requests.exceptions.RequestException, socket.timeout):
            log_output(f"创建多线程下载失败，正在进行第{retry}次重试...")
            time.sleep(3)
            retry += 1
            if retry > 5:
                log_output(f"创建多线程下载失败，重试次数过多，已跳过。")
                return False

    return None

if __name__ == '__main__':

    picUrl = get_all_pic_url()
    multithread_download(picUrl)

    # update_all_artworks(ALL_PATHS) //更新图库
    # traversal_list = all_pids(ALL_PATHS) //废弃
    # multithread_download(picUrl, traversal_list) //废弃


