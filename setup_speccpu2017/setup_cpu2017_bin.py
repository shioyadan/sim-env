# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0303,C0326,R0201,R0903

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
parser = argparse.ArgumentParser(description='SPECCPU2017 binary extractor.')
parser.add_argument('INSTALL_DIR', type=str, help='Specify a SEPCCPU2017 installed directory.')
parser.add_argument('OUTPUT_DIR', type=str, help='Specify a destination directory.')
parser.add_argument('ARCH_PREFIX', type=str, help='Specify an architecure name prefix. This script will output data to data/$(ARCH_PREFIX)')
parser.add_argument('MARKER', type=str, help='Specify a ame maker. This script search files from benchspec/CPU/build/* including this mark')
args = parser.parse_args()

marker = args.MARKER
arch_prefix = args.ARCH_PREFIX
src_root = args.INSTALL_DIR + "/benchspec/CPU"
dst_root = args.OUTPUT_DIR + "/" + arch_prefix + "/bin"

# Simple checking 
if not os.path.exists(src_root):
    print("Error: '%s' is not the installed direcotry of SPECCPU2017." % args.INSTALL_DIR)
    os.sys.exit(1)


bench_list = [
    "600.perlbench_s",  "602.gcc_s",        "603.bwaves_s",     "605.mcf_s",
    "607.cactuBSSN_s",  "619.lbm_s",        "620.omnetpp_s",    "621.wrf_s",
    "623.xalancbmk_s",  "625.x264_s",       "627.cam4_s",       "628.pop2_s",
    "631.deepsjeng_s",  "638.imagick_s",    "641.leela_s",      "644.nab_s",
    "648.exchange2_s",  "649.fotonik3d_s",  "654.roms_s",       "657.xz_s",

    #"500.perlbench_r",  "502.gcc_r",        "503.bwaves_r",     "505.mcf_r",
    #"507.cactuBSSN_r",  "508.namd_r",       "510.parest_r",     "511.povray_r",
    #"519.lbm_r",        "520.omnetpp_r",    "521.wrf_r",        "523.xalancbmk_r",
    #"525.x264_r",       "526.blender_r",    "527.cam4_r",       "531.deepsjeng_r",
    #"538.imagick_r",    "541.leela_r",      "544.nab_r",        "548.exchange2_r",
    #"549.fotonik3d_r",  "554.roms_r",       "557.xz_r",
]

# These binary files are out of rules
execeptional_bin_name_list = {
    "gcc_s": "sgcc",
    "roms_s": "sroms",
    "bwaves_s": "speed_bwaves",
    "pop2_s": "speed_pop2",
}

make_directory(dst_root)

err = False

successful_benchmarks = []
err_benchmarks = []

for name in bench_list:

    # Specify source 
    src_build = "%s/%s/build" % (src_root, name)
    src_dir = ""

    if not os.path.isdir(src_build):
        print("Error: A binary file (%s) seems not to be built." % name)
        err_benchmarks.append(name)
        err = True
        continue

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
        err_benchmarks.append(name)
        err = True
        continue

    # Make a destination binary file name
    #m = re.match("^[\d]+\.(.+)", name)
    #dst = dstRoot + "/" + m.group(1)
    dst = dst_root + "/" + re.sub(r"^[\d]+\.", "", name) # Remove a number prefix

    # Remove a number part and create a name
    raw_name = re.sub(r"\d+\.", "", name)
    if raw_name in execeptional_bin_name_list:
        raw_name = execeptional_bin_name_list[raw_name]
    
    # Copy files
    src_file = src_dir + "/" + raw_name
    if not os.path.exists(src_file):
        print("Error: A binary file (%s) seems not to be built." % raw_name)
        err_benchmarks.append(name)
        err = True
        continue
        
    print("Copying %s to %s" % (src_file, dst))
    shutil.copy2(src_file, dst)
    successful_benchmarks.append(name)

print("Extract successes: %s" % successful_benchmarks)
print("Extract errors: %s" % err_benchmarks)

#if err:
#    os.sys.exit(1)


