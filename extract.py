import re
from log import log_output

def extract_pic_info(response_text, repeat):
    log_output(f"正在处理插画标题...")
    # 通过正则表达式匹配响应文本中的画作标题
    name = re.search('"illustTitle":"(.+?)"', response_text).group(1)
    # 对name进行字符串替换操作，将文件名中不允许出现的字符（包括'\', '/', ':', '*', '?', '"', '<', '>', '|'）用下划线替换，保证后续保存文件时不会出错。
    name = re.sub(r'[\\/:\*\?"<>\|]', '_', name)
    # 对name进行字符串替换操作，如果有多个画作的标题相同，则在文件名末尾添加一个数字（repeat），避免文件名重复。
    name = re.sub(r'[\\/:\*\?"<>\|]', str(repeat), name)
    repeat += 1
    log_output(f"正在处理作者名...")
    user_name = re.search('"userName":"(.+?)"', response_text).group(1)
    user_name = re.sub(r'[\\/:\*\?"<>\|]', '_', user_name)
    user_name = re.sub(r'[\\/:\*\?"<>\|]', str(repeat), user_name)
    repeat += 1
    # 提取图片原图地址
    picture = re.search('"original":"(.+?)"', response_text).group(1)
    pid = re.search('"illustId":"(\d+)"', response_text).group(1)
    return name, user_name, picture, pid, repeat