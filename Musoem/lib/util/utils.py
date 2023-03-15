import re, os

def get_bpm_from_path(path):
    dir_name = os.path.basename(path)
    return re.findall(r'bpm=([0-9]+)', dir_name)
