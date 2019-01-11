import shutil
import re
import argparse
import os
from os.path import join


def make_directory(path):
    """ Create a directory if there is not a specified directory """
    if not os.path.exists(path):
        os.makedirs(path)

def copy_tree(srcDir, dstDir):
    """ Copy a directory tree of srcDir to dstDir """
    print("Copying %s to %s" % (srcDir, dstDir))

    make_directory(dstDir)

    for i in os.listdir(srcDir):
        src = join(srcDir, i)
        dst = join(dstDir, i)
        if os.path.isdir(src):
            copy_tree(src, dst)
        else:
            shutil.copy2(src, dst)

def copy_node(src_dir, dst_dir, name, data_type):
    """ Setup each benchmark data directory
    srcDir: A directory of source data of specified benchmark
        e.g. '(installed dir)/benchspec/CPU2006/400.perlbench/data'
    dstDir: A directory of destination  
        e.g. '.\\data/400.perlbench'
    name: The name of a specified benchmark
        e.g. '400.perlbench'
    dataType: 'test', 'train', or 'ref'
    """

    # Copy merged all/target data
    # Typical benchmarks merge 'test/train/ref' and 'all' directory to setup 
    src_all = "%s/all/input" % src_dir
    src_target = "%s/%s/input" % (src_dir, data_type)
    dst_input = "%s/%s/input" % (dst_dir, data_type)    # A copy destination directory of 'input'

    if os.path.exists(src_all):  # 'gromacs' does not have "all"
        copy_tree(src_all, dst_input)
    if os.path.exists(src_target): # 'namd' does not have "test/train/ref"
        copy_tree(src_target, dst_input)

    # Copy reference output data
    src_output = "%s/%s/output" % (src_dir, data_type)
    dst_output = "%s/%s/output" % (dst_dir, data_type)
    copy_tree(src_output, dst_output)

    src_all_output = "%s/all/output" % src_dir
    if os.path.exists(src_all_output):  # 'gromacs' does not have "all"
        copy_tree(src_all_output, dst_output)


    #
    # Special care for each benchmark program
    #
    if name == "481.wrf":
        # Copy specific RRTM_DATA
        # le/32 is used in amd64
        # le: little endian
        # be: big endian
        src = dst_input + "/le/32/RRTM_DATA"
        dst = dst_input + "/RRTM_DATA"
        shutil.copy2(src, dst)

    if name == "482.sphinx3":
        ctlList = []
        for i in sorted(os.listdir(dst_input)):
            # Copy all *.le.raw to *.raw
            # le: little endian
            # be: big endian
            m = re.search("^(.+)\.le\.(raw)$", i)
            if m:
                src = dst_input + "/" + m.group(0)
                dst = dst_input + "/" + m.group(1) + "." + m.group(2)
                shutil.copy2(src, dst)
                ctlList.append("%s %s\n" % (m.group(1), os.path.getsize(dst)))

        # Making ctlfile of 482.sphinx3
        # This is originally performed in Spec/object.pm
        file = open(dst_input + "/ctlfile", "wt")
        for i in ctlList:
            file.write(i)
        file.close()
        print(file)

# Parse arguments 
parser = argparse.ArgumentParser(description='SPECCPU2006 data extractor.')
parser.add_argument('INSTALL_DIR', type=str, help='Specify a SEPCCPU2006 directory.')
parser.add_argument('OUTPUT_DIR', type=str, help='Specify a destination directory.')
parser.add_argument('MARKER', type=str, help='Specify an architectural name maker. This script search files from benchspec/CPU2006/xxx/build/* including this mark')
args = parser.parse_args()

# Test
# if os.name == "nt":
#    srcRoot = "Z:\\work\\gem5-work\\work\\benchmark\\aarch64\\installed\\benchspec\\CPU2006"
#    dstRoot = ".\\data"
#else:
#    srcRoot = "/home/shioya/work/gem5-work/work/benchmark/aarch64/installed/benchspec/CPU2006"
#    dstRoot = "./data"

marker = args.MARKER
src_root = args.INSTALL_DIR + "/benchspec/CPU2006"
dst_root = args.OUTPUT_DIR + "/" + marker + "/run"

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


dataTypes = ["test", "train", "ref"]

for type in dataTypes:
    for name in bench_list:
        src = "%s/%s/data" % (src_root, name)
        
        # Remove a number prefix
        #dst = "%s/%s" % (dst_root, re.sub("^[\d]+\.", "", name))
        dst = "%s/%s" % (dst_root, name)

        copy_node(src, dst, name, type)

        # Vefication test
        #diffSrc = "%s/%s/run/run_base_%s_amd64-m64-gcc43-nn.0000/" % (srcRoot, name, type)
        #print("diff -r %s/%s/input %s" % (dst, type, diffSrc))