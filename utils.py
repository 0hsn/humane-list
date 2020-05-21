from typing import List
from stat import *
import pwd
import grp
import os
import datetime

class FileInfo:
    def __init__(self, title, permission, type, owner, group, size, modtime):
        self.title = title
        self.permission = permission
        self.type = type
        self.owner = owner
        self.group = group
        self.size = size
        self.modtime = modtime

def check_and_get_file_infos(sys_path: str) -> List[FileInfo]:
    if os.path.exists(sys_path):
        directories = os.listdir(sys_path)
        return __get_file_infos(directories, sys_path)
    else:
        raise FileNotFoundError(f"{sys_path} is not a file or directory")

def __get_merged_dir_path(dirs: List[str], sys_path: str) -> List[str]:
    merged_dirs = []

    t_sys_path = sys_path.rstrip('/')
    index = 0

    while index < len(dirs):
        merged_dirs.append(t_sys_path + '/' + dirs[index])
        index += 1

    merged_dirs.sort()
    return merged_dirs


def __get_file_infos(dirs: List[str], sys_path: str) -> List[FileInfo]:
    file_infos = []
    dirs.sort()

    for dir in dirs:
        stat_res = os.stat(sys_path + '/' + dir)
        file_infos.append(
            FileInfo(
                title=dir,
                permission=__find_perm(stat_res.st_mode),
                type=__find_type(stat_res.st_mode),
                owner=__find_username(stat_res.st_uid),
                group=__find_grpname(stat_res.st_gid),
                size=sizeof_fmt(stat_res.st_size),
                modtime=datetime.datetime.fromtimestamp(stat_res.st_mtime).strftime("%d/%m/%y %H:%M:%S")
            )
        )

    return file_infos


def __find_type(f_mode: int) -> str:
        if S_ISDIR(f_mode):
            return 'DIR'
        elif S_ISREG(f_mode):
            return 'FYL'
        elif S_ISCHR(f_mode):
            return 'CHR'
        elif S_ISBLK(f_mode):
            return 'BLK'
        elif S_ISFIFO(f_mode):
            return 'PYP'
        elif S_ISLNK(f_mode):
            return 'LNK'
        elif S_ISSOCK(f_mode):
            return 'SOC'
        elif S_ISDOOR(f_mode):
            return 'DOR'
        elif S_ISPORT(f_mode):
            return 'PRT'
        elif S_ISWHT(f_mode):
            return 'WHT'
        else:
            return 'UNK'

def __find_username(f_uid: int) -> str:
    return pwd.getpwuid(f_uid).pw_name

def __find_grpname(f_gid: int) -> str:
    return grp.getgrgid(f_gid).gr_name

def __find_perm(f_mode: int) -> str:
    mod_dec = S_IMODE(f_mode)
    return str(oct(mod_dec))[2:]

# https://stackoverflow.com/a/1094933

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
