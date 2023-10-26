import re
import socket
import time
import requests
from conf.config import cookie, referer, PIXIV_DIR, ALL_PATHS, LOGO_PIXIV, HEAD_BARK
from fake_useragent import UserAgent
from log import log_output

headers = {
    'referer': referer,
    'user-agent': UserAgent().random,
    'Cookie': cookie
}


def get_all_pic_url():
    illust_id = []
    log_output(f"开始获取日榜插画...")
    for n in range(1, 10 + 1):
        log_output(f"获取第{n}页插画...")
        retry = 1
        # 使用f-string格式化字符串，更加简洁明了
        url = f'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p={n}&format=json'
        # 获取图片下载链接
        while True:
            try:
                # 使用Session对象，提升请求效率
                with requests.Session() as session:
                    response = session.get(url, headers=headers)
                    illust_id = illust_id + re.findall('"illust_id":(\d+?),', response.text)
                    break
            except (requests.exceptions.RequestException, socket.timeout):
                log_output(f"获取第{n}页插画下载链接，正在进行第{retry}次重试...")
                time.sleep(3)
                retry += 1
                if retry > 5:
                    log_output(f"获取第{n}页插画下载链接失败，重试次数过多，已跳过。")
                    return False
    # 生成图片下载链接列表
    picUrl = ['https://www.pixiv.net/artworks/' + i for i in illust_id]
    log_output(f"获取日榜插画下载链接成功！")
    return picUrl