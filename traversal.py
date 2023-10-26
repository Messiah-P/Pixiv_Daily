import os
from db.artworks import insert, insert_pid_no

Filelist = []

def get_filelist(src_path, Filelist):
    if os.path.isfile(src_path):
        if os.path.basename(src_path) != ".DS_Store":
            if os.path.basename(src_path) != "._.DS_Store":
                Filelist.append(src_path)

    elif os.path.isdir(src_path) and not os.path.basename(src_path) == "@eaDir":
        for s in os.listdir(src_path):
            newDir = os.path.join(src_path, s)
            get_filelist(newDir, Filelist)

    return Filelist



def all_pids(all_path):
    pids = []
    for i in range(len(all_path)):
        filelist = get_filelist(all_path[i], Filelist)

    for file in filelist:
        base_name = os.path.basename(file)
        pid = base_name.split('=')[1].split(']')[0]
        pids.append(pid)

    return pids

#更新全部数据库
def update_all_artworks(all_path):
    pids = []
    for i in range(len(all_path)):
        filelist = get_filelist(all_path[i], Filelist)

    for file in filelist:
        base_name = os.path.basename(file)
        #解析文件名，获取pid和pid_no
        pid = base_name.split('[pid=')[1].split(']')[0]
        # 检查是否包含 ']-p' 和 '.jpg'
        if ']-p' in base_name and '.jpg' in base_name:
            # 执行字符串操作
            #print(pid + "有子图")
            pid_no = base_name.split(']-p')[1].split('.jpg')[0]
            # 将数据插入到名为 'artworks' 的表中
            data = [{'pid': pid, 'pid_no': pid_no}]
            insert_pid_no('artworks', data, pid, pid_no)
        elif ']-p' in base_name and '.png' in base_name:
            # 执行字符串操作
            #print(pid + "有子图")
            pid_no = base_name.split(']-p')[1].split('.png')[0]
            # 将数据插入到名为 'artworks' 的表中
            data = [{'pid': pid, 'pid_no': pid_no}]
            insert_pid_no('artworks', data, pid, pid_no)
        else:
            # 如果字符串不包含所需子字符串，可以选择执行默认操作或者报错
            #print(pid+"无子图")
            # 示例用法，将数据插入到名为 'artworks' 的表中
            data = [{'pid': pid}]
            insert('artworks', data, pid)

        pids.append(pid)
    return pids