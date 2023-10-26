import datetime
import yaml
import os

# 读取YAML文件
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir,"config.yml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# 获取Headers配置
headers = config["headers"]
cookie = headers["cookie"]
referer = headers["referer"]

# 获取Paths配置
paths = config["paths"]
PIXIV_DIR = paths["pixiv_dir"] #日榜插画的保存路径
ALL_PATHS = paths["all_pic"] #所有图片的保存路径
LOG_PATH = paths["log_path"]

# 链接配置
links = config["links"]
LOGO_PIXIV = links["logo_pixiv"]
HEAD_BARK = links["head_bark"]

#其他信息
time_now = datetime.datetime.now()
time_yesterday = time_now + datetime.timedelta(days=-1)
log_path = f"{LOG_PATH}/{datetime.datetime.now():%Y-%m-%d}.log"


