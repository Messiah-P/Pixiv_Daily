import requests
import re
import datetime
import traversal
import os, sys, stat
import logging
import unittest
from fake_useragent import UserAgent
#import paramiko

headers = {
    'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
    'user-agent': UserAgent(verify_ssl=False).random,
    'Cookie': '_im_vid=01GQCX73FXBEW22BB0WVHXR401; _fbp=fb.1.1674396763223.37132445; __utma=235335808.1116251316.1674396762.1674633889.1674656386.6; __utmb=235335808.2.10.1674656386; __utmc=235335808; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=90529190=1^9=p_ab_id=1=1^10=p_ab_id_2=4=1^11=lang=zh=1; __utmz=235335808.1674401888.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.1.1116251316.1674396762; _ga_75BBYNYN9J=GS1.1.1674656386.8.1.1674656397.0.0.0; __cf_bm=gnWlhNz.PSVZFqm8knxxpYeu081yn7xqmO7Ndyjj9Gc-1674656387-0-AQvlSyLXn5MVr2+N7386shXLF/Fsb12B3niWAwk/fLNMMUrMs+XoPtP9knuAah3egT90ehXdVYxgNEMLqjg3jDGcXLS4Mbfyn+Da93upWYIsSuBCzGYk7/WC/Y5wr6VRJETj2SoKfZl7dsPu94POi1YzMKqdnQHTottKwrrWAuwbfNc6WMJUcAT1tF4K08H3glFY1P833C5pLm11hT8MmN0=; PHPSESSID=90529190_jkIDly6jy9CkhsFWoA5kjokanoEqQkEn; __utmt=1; a_type=0; b_type=1; c_type=22; privacy_policy_notification=0; _ga_MZ1NL4PHH0=GS1.1.1674633912.3.1.1674633965.0.0.0; device_token=aa64336f330ae88c207814dca2c5ced1; privacy_policy_agreement=5; _gid=GA1.2.235656553.1674582691; tag_view_ranking=Lt-oEicbBr~RTJMXD26Ak~uW5495Nhg-~yTFlPOVybE~7ebIzNRkdM~b3tIEUsHql~Qw2RLEQgKY~jH0uD88V6F~jhuUT0OJva~EZQqoW9r8g~PEWvBxU9pH~-t_IAEknVh~RlJg_oCwwz~EmhsFxSBo-~R4YyPA5U1t~QOlvfk_Wxj~hvsnPcI8Rg~D0nMcn6oGk~_pwIgrV8TB~p76wqGJbIo~uusOs0ipBx~lKmQRiaEov~YRDwjaiLZn~5WlN6qpDZj~1HD6lhXO_A~9PI9msRK8Q~mv-jOivdpn~ZKYx1SDf_f~pnCQRVigpy~5NIG-P_d-D; cto_bundle=qGJ8Zl9uaGtIJTJCNkZISmI1ZzJVcHBsNGgzckU5YzN4WFJPRlZoN3J3RXNnUW5FOFpvbTFhJTJGZXViTWt4Qm8lMkYlMkJWYURIa3k2MGxVZFpjWFFPYU1IJTJGbURGSzBOZGxVVm9NRHJxWmNsY0wxQWpzZmlyUzEzbGlLNFRiQWc5UGFsTFpxNVIlMkZIeVhWN3djWGhQMGd6bndOSjdRajZGNlZDUDhDUGFsaDZqY0Y5ZHdIT3R0dGclM0Q; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; login_ever=yes; p_ab_d_id=702090925; p_ab_id=1; p_ab_id_2=4; first_visit_datetime_pc=2022-12-27+09%3A50%3A49; yuid_b=OWEnNRA'
}

proxy = {import time
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

    #'http': 'http://proxy.pantheon.center:7893',
    #'https': 'http://60.143.43.45:3128'
}

path = '/mnt/photo/Pixiv'
all_path = ['/mnt/photo/Pixiv', '/mnt/photo/画师']
logo_pixiv = 'https://lsky.pantheon.center/image/2022/11/20/637a374fa4aca.jpeg'
head_bark = 'https://bark.pantheon.center/WSeN8LCGbCDZqHAJMTmeHP'
#print(type(head_bark))
repeat = 1
time_now = datetime.datetime.now()
time_yesterday = time_now + datetime.timedelta(days=-1)
log = str(time_now.year)+'-'+str(time_now.month)+'-'+str(time_now.day)
log_path = '/mnt/nas/Config/Log/Pixiv/%s.log'% log

def getSinglePic(url, count):
    global repeat
    #time_now = datetime.now()
    response = requests.get(url, headers=headers, timeout = (3,17))# proxies = proxy,
    # 提取图片名称
    name = re.search('"illustTitle":"(.+?)"', response.text)
    name = name.group(1)
    if re.search('[\\\ \/ \* \? \" \: \< \> \|]', name) != None:
        name = re.sub('[\\\ \/ \* \? \" \: \< \> \|]', str(repeat), name)
        repeat += 1
    # 提取作者名称
    userName = re.search('"userName":"(.+?)"', response.text)
    userName = userName.group(1)
    if re.search('[\\\ \/ \* \? \" \: \< \> \|]', userName) != None:
        userName = re.sub('[\\\ \/ \* \? \" \: \< \> \|]', str(repeat), userName)
        repeat += 1
    # 提取图片原图地址
    #picture = re.search('"original":"(.+?)"},"tags"', response.text)
    picture = re.search('"original":"(.+?)"', response.text)
    pic = requests.get(picture.group(1), headers=headers)
    PATH = os.path.join(path, str(time_yesterday.year), str(time_yesterday.month), str(time_yesterday.day)+"_daily")
    os.makedirs(PATH, 0o777, exist_ok=True)
    pid = url.split('/')[4]
    with open(log_path, 'a+') as l:
        print('[' + str(time_now).split('.')[0] + ']' + '图名=%d - %s - %s[pid=%s].%s' % (count, userName, name, pid, picture.group(1)[-3:]), end=',', file = l)
        print('[' + str(time_now).split('.')[0] + ']' + '图名=%d - %s - %s[pid=%s].%s' % (count, userName, name, pid, picture.group(1)[-3:]), end=',')
    PATH = PATH + '/%d - %s - %s[pid=%s].%s' % (count, userName, name, pid, picture.group(1)[-3:])
    f = open(PATH, 'wb')
    f.write(pic.content)
    os.chmod(PATH, 0o777)
    f.close()


def getAllPicUrl():
    count = 1
    valid_count = 0
    invalid_count = 0
    traversal_list = traversal.all_pids(all_path)
    for n in range(1, 10 + 1):
        url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=%d&format=json' % n
        #response = requests.get(url, headers=headers, proxies = proxy)
        response = requests.get(url, headers=headers)
        illust_id = re.findall('"illust_id":(\d+?),', response.text)
        picUrl = ['https://www.pixiv.net/artworks/' + i for i in illust_id]
        #with open('pixiv.log', 'a+') as l:
        for url in picUrl:
            if count <= 50:
                pid = url.split('/')[4]
                #time_now = datetime.now()
                if pid not in traversal_list:
                    with open(log_path, 'a+') as l:
                        print('[' + str(time_now).split('.')[0] + ']' + '正在下载第%d张图片'% count, file=l)
                        print('[' + str(time_now).split('.')[0] + ']' + '正在下载第%d张图片'% count)
                    print(url)
                    getSinglePic(url, count)
                    with open(log_path, 'a+') as l:
                        print('下载成功!', file=l)
                        print('下载成功!')
                        os.chmod(log_path, 0o777)
                    count += 1
                    valid_count += 1
                else:
                    with open(log_path, 'a+') as l:
                        print('[' + str(time_now).split('.')[0] + ']'+'第%d张图片(pid=%s),重复跳过!'% (count, pid), file=l)
                        print('[' + str(time_now).split('.')[0] + ']'+'第%d张图片(pid=%s),重复跳过!'% (count, pid))
                        os.chmod(log_path, 0o777)
                    count += 1
                    invalid_count += 1
            else:
                break
    ret = requests.get('%s/Pixiv日榜更新/成功获取新图：%d张\n重复：%d张?icon=%s&group=Pixiv'% (head_bark,valid_count,invalid_count,logo_pixiv))
    return None

if __name__ == '__main__':
    getAllPicUrl()
