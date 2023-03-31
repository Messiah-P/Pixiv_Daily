import os

Filelist = []

def get_filelist(src_path, Filelist):
    if os.path.isfile(src_path):
        if os.path.basename(src_path) !=".DS_Store":
            if os.path.basename(src_path) != "._.DS_Store":
                Filelist.append(src_path)

    elif os.path.isdir(src_path):
        for s in os.listdir(src_path):
            newDir = os.path.join(src_path, s)
            get_filelist(newDir, Filelist)

    return Filelist


def all_pids(all_path):
    for i in range(len(all_path)):
        filelist = get_filelist(all_path[i], Filelist)
        pids = []

    for file in filelist:
        base_name = os.path.basename(file)
        pid = base_name.split('=')[1].split(']')[0]
        pids.append(pid)

    return pids
