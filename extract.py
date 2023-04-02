import re

def extract_pic_info(response_text):
    # 提取图片名称
    name = re.search('"illustTitle":"(.+?)"', response_text).group(1)
    name = re.sub(r'[\\/:\*\?"<>\|]', '_', name)
    # 提取作者名称
    user_name = re.search('"userName":"(.+?)"', response_text).group(1)
    user_name = re.sub(r'[\\/:\*\?"<>\|]', '_', user_name)
    # 提取图片原图地址
    picture = re.search('"original":"(.+?)"', response_text).group(1)
    pid = re.search('"illustId":"(\d+)"', response_text).group(1)
    return name, user_name, picture, pid