import os, shutil
from FoxDot import SYNTHDEF_DIR as FOXDOT_SYNTHS_DIR
from .base.constants import *

def copy_synths():
    for file in os.listdir(MUSOEM_SYNTHS_DIR):
        src = MUSOEM_SYNTHS_DIR + "/" + file
        dst = FOXDOT_SYNTHS_DIR + "/" + file
        shutil.copyfile(src, dst)
copy_synths()
