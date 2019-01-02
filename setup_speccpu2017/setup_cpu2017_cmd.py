# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0303,C0326,R0201,R0903

#import shutil
import re
import argparse
import json
import sys
import os
#from os.path import join


def make_directory(path):
    """ Create a directory if there is not a specified directory """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


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


def parse_command_input(line):
    """ Parse arguments in a SPEC command file """

    tokens = re.split(r"\s+", line)
    info = {
        "stdin": "",
        "stdout": "",
        "stderr": "",
        "bin": "",
        "args":  "",
        "work": ""
    }

    i = 0
    while i < len(tokens):
        if tokens[i] == "-i":
            info["stdin"] = tokens[i + 1]
            i += 1
        elif tokens[i] == "-o":
            info["stdout"] = tokens[i + 1]
            i += 1
        elif tokens[i] == "-e":
            info["stderr"] = tokens[i + 1]
            i += 1
        else: 
            # Since there is a binary file name just after -i/-o/-e, 
            # it exits the loop.
            info["bin"] = tokens[i]
            i += 1
            break
        i += 1
    
    # stdin/stdout/stderr specified by -i/-o/-e must match "<"/">"/"2>>"
    args = []
    while i < len(tokens):
        if tokens[i] == "<":
            if info["stdin"] != tokens[i + 1]:
                print("stdin mismatch: '-i %s' != '< %s'" % info["stdin"] != tokens[i + 1])
            i += 1
        elif tokens[i] == ">":
            info["stdout"] = tokens[i + 1]
            if info["stdout"] != tokens[i + 1]:
                print("stdout mismatch: '-o %s' != '> %s'" % info["stdin"] != tokens[i + 1])
            i += 1
        elif tokens[i] == "2>>":
            info["stderr"] = tokens[i + 1]
            if info["stderr"] != tokens[i + 1]:
                print("stderr mismatch: '-e %s' != '2>> %s'" % info["stdin"] != tokens[i + 1])
            i += 1
        else: 
            if tokens[i] != "":
                args.append(tokens[i])
        i += 1

    info["args"] = args

    return info


def output_command_file(file_name, info):
    """ Write a command file as a json"""
    data = {
        "session": {
            "processes": {
                "process": info
            }
        }
    }
    json_data = json.dumps(data, sort_keys=True, indent=2)

    file = open(file_name, "w")
    file.writelines(json_data)
    file.close()


def main():
    """ main rountine """

    # Parse arguments 
    parser = argparse.ArgumentParser(description='SPECCPU2017 data extractor.')
    parser.add_argument('INSTALL_DIR', type=str, help='Specify a SEPCCPU2017 directory.')
    parser.add_argument('OUTPUT_DIR', type=str, help='Specify a destination directory.')
    parser.add_argument('ARCH_PREFIX', type=str, help='Specify an architecure name prefix. This script will output data to data/$(ARCH_PREFIX)')
    parser.add_argument('MARKER', type=str, 
        help='Specify an architectural name maker. This script search files from benchspec/CPU2017/xxx/run/* including this mark')
    args = parser.parse_args()

    marker = args.MARKER
    arch_prefix = args.ARCH_PREFIX
    src_root = args.INSTALL_DIR + "/benchspec/CPU"
    dst_dir = args.OUTPUT_DIR + "/" + arch_prefix + "/cmd"
    bin_dir = args.OUTPUT_DIR + "/" + arch_prefix + "/bin"
    run_dir = args.OUTPUT_DIR + "/" + arch_prefix + "/run"

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
    data_types = ["test", "train", "refspeed"]

    # Make output directory
    make_directory(dst_dir)

    # Initialize command tables
    diff_commands = {}
    clean_commands = {}
    input_diff_commands = {}
    for name in bench_list:
        for data_type in data_types:
            key = name + "-" + data_type
            diff_commands[key] = []
            clean_commands[key] = []
            input_diff_commands[key] = []

    successful_benchmarks = []
    err_benchmarks = []

    for name in bench_list:

        # Specify source 
        src_run = "%s/%s/run" % (src_root, name)

        # Remove a number prefix
        # raw_name = re.sub(r"^[\d]+\.", "", name) 
        # Don't remove a number prefix
        raw_name = name 

        for data_type in data_types:

            # Find a run directory
            src_dir = find_run_directory(src_run, data_type, marker)
            if src_dir == "":
                err_benchmarks.append(name)
                continue

            # Parse command file
            cmd_file = open(src_dir + "/speccmds.cmd")
            index = 0
            for line in cmd_file.readlines():

                # Some commands are skipped
                # C: directory command
                # E: environemental value
                # R,N: ???
                if re.match(r"\-[CcEeRrNn]", line):    
                    continue

                if re.match(r"\-[^ioe]", line):    
                    print("Could not parse speccmds.cmd in %s: %s" % (name, line))

                # Parse arguments
                info = parse_command_input(line)

                # Make a destination command file name
                dst = "%s/%s-%s.%d.json" % (dst_dir, raw_name, data_type, index)
                index += 1

                # bin/work path is specified by a relative path
                bin_name = bin_dir + "/" + re.sub(r"^[\d]+\.", "", raw_name) 
                work = run_dir + "/" + raw_name + "/" + data_type + "/input"
                info["bin"] = os.path.relpath(bin_name, dst_dir)
                info["work"] = os.path.relpath(work, dst_dir)

                # Output a file
                output_command_file(dst, info)
                print(".", end="")
                sys.stdout.flush() # flush=True is not supported in 3.2

                # Add input diff
                verify_file_name = raw_name + "-" + data_type
                diff = "diff -r -s %s %s \n" % (src_dir, info["work"])
                input_diff_commands[verify_file_name].append("echo -- %s/%s\n" % (raw_name, data_type))
                input_diff_commands[verify_file_name].append(diff)

            cmd_file.close()


            # Parse compare file
            cmp_file = open(src_dir + "/compare.cmd")
            for line in cmp_file.readlines():
                # Skip commands
                if re.match(r"\-[CcEeRrNnOo]", line):    
                    continue

                if not re.match(r"\-[k]", line):    
                    print(r"Could not parse compare.cmd in %s: %s" % (name, line))

                m = re.search(r"([^\s]+)[\s]+>[\s]+([^\s]+)[\s\n]*$", line)
                if not m:
                    print(r"Could not parse compare.cmd in %s: %s" % (name, line))
                target_file = m.group(1)
                
                full_target_dir = run_dir + "/" + raw_name + "/" + data_type
                rel_target_dir = os.path.relpath(full_target_dir, dst_dir)

                verify_file_name = raw_name + "-" + data_type

                # Make diff commannds
                diff = "diff -s %s/input/%s %s/output/%s\n" % (
                    rel_target_dir, target_file,
                    rel_target_dir, target_file,
                )
                diff_commands[verify_file_name].append("echo " + diff)
                diff_commands[verify_file_name].append(diff)

                # Make clean commands
                clean = "rm -f %s/input/%s\n" % (rel_target_dir, target_file)
                clean_commands[verify_file_name].append("echo " + clean)
                clean_commands[verify_file_name].append(clean)

            cmp_file.close()

            successful_benchmarks.append(name)

    #
    for data_type in diff_commands:
        file_name = "%s/verify_output_%s.sh" % (dst_dir, data_type)
        file = open(file_name, "w")
        file.writelines(diff_commands[data_type])
        file.close()

    for data_type in input_diff_commands:
        file_name = "%s/verify_input_%s.sh" % (dst_dir, data_type)
        file = open(file_name, "w")
        file.writelines(input_diff_commands[data_type])
        file.close()

    for data_type in clean_commands:
        file_name = "%s/clean_%s.sh" % (dst_dir, data_type)
        file = open(file_name, "w")
        file.writelines(clean_commands[data_type])
        file.close()

    print("\n")
    print("Extract successes: %s" % successful_benchmarks)
    print("Extract errors: %s" % err_benchmarks)

# Entry point
main()
