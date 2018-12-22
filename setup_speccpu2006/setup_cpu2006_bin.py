import shutil
import re
import argparse
import os
from os.path import join


def make_directory(path):
    """ Create a directory if there is not a specified directory """
    if not os.path.exists(path):
        os.makedirs(path)

# Parse arguments 
parser = argparse.ArgumentParser(description='SPECCPU2006 binary extractor.')
parser.add_argument('INSTALL_DIR', type=str, help='Specify a SEPCCPU2006 installed directory.')
parser.add_argument('OUTPUT_DIR', type=str, help='Specify a destination directory.')
parser.add_argument('MARKER', type=str, help='Specify an architectural name maker. This script search files from benchspec/CPU2006/xxx/build/* including this mark')
args = parser.parse_args()

marker = args.MARKER
src_root = args.INSTALL_DIR + "/benchspec/CPU2006"
dst_root = args.OUTPUT_DIR + "/" + marker + "/bin"

# Simple checking 
if not os.path.exists(src_root):
    print("Error: '%s' is not the installed direcotry of SPECCPU2006." % args.INSTALL_DIR)
    os.sys.exit(1)


bench_list = [
    "400.perlbench",  "435.gromacs",    "454.calculix",    "471.omnetpp",    
    "401.bzip2",      "436.cactusADM",  "456.hmmer",       "473.astar",
    "403.gcc",        "437.leslie3d",   "458.sjeng",       "481.wrf",
    "410.bwaves",     "444.namd",       "459.GemsFDTD",    "482.sphinx3",    
    "416.gamess",     "445.gobmk",      "462.libquantum",  "483.xalancbmk",  
    "429.mcf",        "447.dealII",     "464.h264ref",
    "433.milc",       "450.soplex",     "465.tonto",
    "434.zeusmp",     "453.povray",     "470.lbm",
]

# These binary files are out of rules
execeptional_bin_name_list = {
    "sphinx3": "sphinx_livepretend",
    "xalancbmk": "Xalan"
}

make_directory(dst_root)

err = False

for name in bench_list:

    # Specify source 
    src_build = "%s/%s/build" % (src_root, name)
    src_dir = ""

    # Find the latest build directory
    latest_time = 0
    for i in os.listdir(src_build):
        dir = src_build + "/" + i
        if not os.path.isdir(dir):
            continue
        if not re.search(marker, i):
            continue

        time = os.path.getmtime(dir)
        if latest_time < time:
            latest_time = time
            src_dir = dir

    if src_dir == "":
        print("Error: A binary file (%s) seems not to be built." % name)
        err = True
        continue

    # Make a destination binary file name
    #m = re.match("^[\d]+\.(.+)", name)
    #dst = dstRoot + "/" + m.group(1)
    dst = dst_root + "/" + re.sub("^[\d]+\.", "", name) # Remove a number prefix

    # Remove a number part and create a name
    raw_name = re.sub("\d+\.", "", name)
    if raw_name in execeptional_bin_name_list:
        raw_name = execeptional_bin_name_list[raw_name]
    
    # Copy files
    src_file = src_dir + "/" + raw_name
    if not os.path.exists(src_file):
        print("Error: A binary file (%s) seems not to be built." % raw_name)
        err = True
        continue
        
    print("Copying %s to %s" % (src_file, dst))
    shutil.copy2(src_file, dst)


#if err:
#    os.sys.exit(1)
