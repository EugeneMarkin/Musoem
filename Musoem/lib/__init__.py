import os, shutil
from FoxDot import SYNTHDEF_DIR as FOXDOT_SYNTHS_DIR

MUSOEM_ROOT_DIR = os.path.realpath(__file__ + "/../..")
MUSOEM_SYNTHS_DIR = MUSOEM_ROOT_DIR + "/lib/synths"

def copy_synths():
    print("copy synths")
    for file in os.listdir(MUSOEM_SYNTHS_DIR):
        src = MUSOEM_SYNTHS_DIR + "/" + file
        dst = FOXDOT_SYNTHS_DIR + "/" + file
        shutil.copyfile(src, dst)
copy_synths()
