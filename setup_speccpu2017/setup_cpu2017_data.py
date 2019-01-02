# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0303,C0326,R0201,R0903

""" SPEC CPU 2017 data extraction program """

import shutil
import re
import argparse
import os
from os.path import join


def make_directory(path):
    """ Create a directory if there is not a specified directory """
    if not os.path.exists(path):
        os.makedirs(path)


def copy_tree(src_dir, dst_dir):
    """ Copy a directory tree of srcDir to dstDir """
    print("Copying %s to %s" % (src_dir, dst_dir))

    make_directory(dst_dir)

    for i in os.listdir(src_dir):
        src = join(src_dir, i)
        dst = join(dst_dir, i)
        if os.path.isdir(src):
            copy_tree(src, dst)
        else:
            shutil.copy2(src, dst)


def find_run_directory(src_run, data_type, maker):
    """ Find the most recently updated and matched directory """

    updated_time = 0
    src_dir = ""

    if not os.path.isdir(src_run):
        print("Error: '%s' seems not to be built. Skip it." % (src_run))
        return ""

    for i in os.listdir(src_run):
        # Check a data type
        # The directory name includes type name
        if not re.search(data_type, i):
            continue
        
        # Skip if this path does not include a maker 
        if not re.search(maker, i):
            continue

        # Skip if this is a file        
        src_test = src_run + "/" + i
        if not os.path.isdir(src_test):
            continue

        # Find the latest directory
        mtime = os.stat(src_test).st_mtime
        if updated_time == 0 or updated_time < mtime:
            updated_time = mtime
            src_dir = src_test

    if src_dir == "":
        print("Error: A 'run' directory (%s) seems not to be built in '%s'. Skip it." % (data_type, src_run))
        return ""

    return src_dir



def copy_node(src_root, dst_dir, name, mapped_name, data_type, mapped_data_type, marker):
    """ Setup each benchmark data directory
    src_root: the path to "run" directory in installed SPEC CPU (benchspec/CPU/)
    dst_dir:  destination directory path
    name:     benchmark name
    mapped_name: A mapped target directory. Some benchmark data directory is 
                 mapped to a directory like "600.perlbench_s" -> "500.perlbench_s"
    data_type: test, train, refspeed
    mapped_data_type: test, train, refspeed -> refrate
    """
    # Copied input data from the "run" directory
    src_run_base = src_root + "/" + name + "/run"
    src_run = find_run_directory(src_run_base, data_type, marker)
    if src_run == "":
        return False

    dst_input = "%s/%s/input" % (dst_dir, data_type)    # A copy destination directory of 'input'
    copy_tree(src_run, dst_input)

    # Copy reference output data from the "benchspec" directory
    src_output = "%s/%s/data/%s/output" % (src_root, mapped_name, mapped_data_type)
    dst_output = "%s/%s/output" % (dst_dir, data_type)
    copy_tree(src_output, dst_output)

    src_all_output = "%s/%s/all/output" % (src_root, mapped_name)
    if os.path.exists(src_all_output):  # 'gromacs' does not have "all"
        copy_tree(src_all_output, dst_output)

    return True

def main():
    """ main rountine """ 

    # Parse arguments 
    parser = argparse.ArgumentParser(description='SPECCPU2017 data extractor.')
    parser.add_argument('INSTALL_DIR', type=str, help='Specify a SEPCCPU2017 directory.')
    parser.add_argument('OUTPUT_DIR', type=str, help='Specify a destination directory.')
    parser.add_argument('ARCH_PREFIX', type=str, help='Specify an architecure name prefix. This script will output data to data/$(ARCH_PREFIX)')
    parser.add_argument('MARKER', type=str, help='Specify an architectural name maker. This script search files from benchspec/CPU/xxx/build/* including this mark')
    args = parser.parse_args()

    # Test
    # if os.name == "nt":
    #    srcRoot = "Z:\\work\\gem5-work\\work\\benchmark\\aarch64\\installed\\benchspec\\CPU2017"
    #    dstRoot = ".\\data"
    #else:
    #    srcRoot = "/home/shioya/work/gem5-work/work/benchmark/aarch64/installed/benchspec/CPU2017"
    #    dstRoot = "./data"

    marker = args.MARKER
    arch_prefix = args.ARCH_PREFIX
    src_root = args.INSTALL_DIR + "/benchspec/CPU"
    dst_root = args.OUTPUT_DIR + "/" + arch_prefix + "/run"

    # Simple checking 
    if not os.path.exists(src_root):
        print("Error: '%s' is not the installed direcotry of SPECCPU2017." % args.INSTALL_DIR)
        os.sys.exit(1)


    # Data source mapping
    bench_map = {
        "600.perlbench_s":  { "source": "500.perlbench_r",  "data_map": { "refspeed": "refrate" } },
        "602.gcc_s":        { "source": "502.gcc_r" },
        "603.bwaves_s":     { "source": "503.bwaves_r" },
        "605.mcf_s":        { "source": "505.mcf_r" },
        "607.cactuBSSN_s":  { "source": "507.cactuBSSN_r" },
        "619.lbm_s":        { "source": "619.lbm_s" },          # dedicated data for _s exists
        "620.omnetpp_s":    { "source": "520.omnetpp_r",    "data_map": { "refspeed": "refrate" } },
        "621.wrf_s":        { "source": "521.wrf_r" },
        "623.xalancbmk_s":  { "source": "523.xalancbmk_r",  "data_map": { "refspeed": "refrate" } },
        "625.x264_s":       { "source": "525.x264_r",       "data_map": { "refspeed": "refrate" } },   
        "627.cam4_s":       { "source": "527.cam4_r" },
        "628.pop2_s":       { "source": "628.pop2_s" },         # _r does not exists
        "631.deepsjeng_s":  { "source": "631.deepsjeng_s" },    # dedicated data for _s exists
        "638.imagick_s":    { "source": "538.imagick_r" },
        "641.leela_s":      { "source": "541.leela_r",      "data_map": { "refspeed": "refrate" } },
        "644.nab_s":        { "source": "544.nab_r" },
        "648.exchange2_s":  { "source": "548.exchange2_r",  "data_map": { "refspeed": "refrate" } },
        "649.fotonik3d_s":  { "source": "549.fotonik3d_r" },
        "654.roms_s":       { "source": "554.roms_r" },
        "657.xz_s":         { "source": "557.xz_r" },

        #"500.perlbench_r",  "502.gcc_r",        "503.bwaves_r",     "505.mcf_r",
        #"507.cactuBSSN_r",  "508.namd_r",       "510.parest_r",     "511.povray_r",
        #"519.lbm_r",        "520.omnetpp_r",    "521.wrf_r",        "523.xalancbmk_r",
        #"525.x264_r",       "526.blender_r",    "527.cam4_r",       "531.deepsjeng_r",
        #"538.imagick_r",    "541.leela_r",      "544.nab_r",        "548.exchange2_r",
        #"549.fotonik3d_r",  "554.roms_r",       "557.xz_r",
    }

    data_type_list = ["test", "train", "refspeed"]

    successful_benchmarks = []
    err_benchmarks = []

    for name in bench_map:
        bench = bench_map[name]

        data_map = {}
        if "data_map" in bench:
            data_map = bench["data_map"]

        for data_type in data_type_list:
            # Remove a number prefix
            #dst = "%s/%s" % (dst_root, re.sub(r"^[\d]+\.", "", name))
            # Ouput a number prefix
            dst = "%s/%s" % (dst_root, name)

            # refrate -> refspeed if necessary
            mapped_data_type = data_type
            if data_type in data_map:
                mapped_data_type = data_map[data_type]
            mapped_name = bench["source"]

            success = copy_node(src_root, dst, name, mapped_name, data_type, mapped_data_type, marker)
            if success:
                successful_benchmarks.append(name + "-" + data_type)
            else:
                err_benchmarks.append(name + "-" + data_type)

            # Vefication test
            #diffSrc = "%s/%s/run/run_base_%s_amd64-m64-gcc43-nn.0000/" % (srcRoot, name, type)
            #print("diff -r %s/%s/input %s" % (dst, type, diffSrc))

    print("Extract successes: %s" % successful_benchmarks)
    print("Extract errors: %s" % err_benchmarks)

main()
