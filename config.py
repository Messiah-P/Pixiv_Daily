import yaml


def read_config():
    # 读取YAML文件
    with open("/mnt/python/Pixiv/Pixiv_Daily/config.yml", "r") as f:
        config = yaml.safe_load(f)

    # 获取Headers配置
    headers = config["headers"]
    cookie = headers["cookie"]
    referer = headers["referer"]

    # 获取Paths配置
    paths = config["paths"]
    pixiv_dir = paths["pixiv_dir"] #日榜插画的保存路径
    all_pic = paths["all_pic"] #所有图片的保存路径

    # 链接配置
    links = config["links"]
    logo_pixiv = links["logo_pixiv"]
    head_bark = links["head_bark"]

    return cookie, referer, pixiv_dir, all_pic, logo_pixiv, head_bark