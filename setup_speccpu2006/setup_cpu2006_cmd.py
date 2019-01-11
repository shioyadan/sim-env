import shutil
import re
import argparse
import json
import sys
import os
from os.path import join


def make_directory(path):
    """ Create a directory if there is not a specified directory """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def find_run_directory(src_run, type, maker):
    """ Find the most recently updated and matched directory """

    updated_time = 0
    src_dir = ""
    for i in os.listdir(src_run):
        # Check a data type
        # The directory name includes type name
        if not re.search(type, i):
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
        print("Error: A 'run' directory (%s) seems not to be built in '%s'. Skip it." % (type, src_run))
        return ""

    return src_dir


def parse_command_input(line):
    """ Parse arguments in a SPEC command file """

    tokens = re.split("\s+", line)
    info = {
        "stdin": "",
        "stdout": "",
        "stderr": "",
        "bin": "",
        "args":  "",
        "work": ""
    }

    i = 0
    while(i < len(tokens)):
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
            info["bin"] = tokens[i]
            i += 1
            break
        i += 1
    
    args = ""
    while(i < len(tokens)):
        args += tokens[i] + " "
        i += 1
    args = args.strip()
    info["args"] = args.split(" ")

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

    # Parse arguments 
    parser = argparse.ArgumentParser(description='SPECCPU2006 data extractor.')
    parser.add_argument('INSTALL_DIR', type=str, help='Specify a SEPCCPU2006 directory.')
    parser.add_argument('OUTPUT_DIR', type=str, help='Specify a destination directory.')
    parser.add_argument('MARKER', type=str, help='Specify an architectural name maker. This script search files from benchspec/CPU2006/xxx/run/* including this mark')
    args = parser.parse_args()

    marker = args.MARKER
    src_root = args.INSTALL_DIR + "/benchspec/CPU2006"
    dst_dir = args.OUTPUT_DIR + "/" + marker + "/cmd"
    bin_dir = args.OUTPUT_DIR + "/" + marker + "/bin"
    run_dir = args.OUTPUT_DIR + "/" + marker + "/run"
    verify_dir = args.OUTPUT_DIR + "/" + marker + "/verify"

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
    data_types = ["test", "train", "ref"]

    # Make output directory
    make_directory(dst_dir)
    make_directory(verify_dir)

    # Initialize command tables
    diff_commands = {}
    clean_commands = {}
    for name in bench_list:
        for data_type in data_types:
            key = name + "-" + data_type
            diff_commands[key] = []
            clean_commands[key] = []

    for name in bench_list:

        # Specify source 
        src_run = "%s/%s/run" % (src_root, name)

        # Remove a number prefix
        #raw_name = re.sub("^[\d]+\.", "", name) 
        raw_name = name

        bin = bin_dir + "/" + re.sub("^[\d]+\.", "", name) 
        for type in data_types:

            # Find a run directory
            src_dir = find_run_directory(src_run, type, marker)
            if src_dir == "":
                continue

            # Parse command file
            cmd_file = open(src_dir + "/speccmds.cmd")
            index = 0
            for line in cmd_file.readlines():

                # A directory command is skipped
                if re.match("\-[Cc]", line):
                    continue

                # Parse arguments
                info = parse_command_input(line)

                # Make a destination command file name
                dst = "%s/%s-%s.%d.json" % (dst_dir, raw_name, type, index)
                index += 1

                # bin/work path is specified by a relative path
                bin = bin_dir + "/" +  re.sub("^[\d]+\.", "", name) 
                work = run_dir + "/" + raw_name + "/" + type + "/input"
                info["bin"] = os.path.relpath(bin, dst_dir)
                info["work"] = os.path.relpath(work, dst_dir)

                # Output a file
                output_command_file(dst, info)
                print(".", end="")
                sys.stdout.flush() # flush=True is not supported in 3.2

            cmd_file.close()


            # Parse compare file
            cmp_file = open(src_dir + "/compare.cmd")
            for line in cmp_file.readlines():
                m = re.search(" ([^\s]+)[\s\n]*$", line)
                target_file = m.group(1)
                
                full_target_dir = run_dir + "/" + raw_name + "/" + type
                rel_target_dir = os.path.relpath(full_target_dir, dst_dir)

                # Make diff commannds
                diff = "diff -w %s/input/%s %s/output/%s\n" % (
                    rel_target_dir, target_file,
                    rel_target_dir, target_file,
                )
                verify_file_name = raw_name + "-" + type
                diff_commands[verify_file_name].append("echo " + diff)
                diff_commands[verify_file_name].append(diff)

                # Make clean commands
                clean = "rm -f %s/input/%s\n" % (rel_target_dir, target_file)
                clean_commands[verify_file_name].append("echo " + clean)
                clean_commands[verify_file_name].append(clean)

            cmp_file.close()

    #
    for type in diff_commands.keys():
        file_name = "%s/verify_%s.sh" % (verify_dir, type)
        file = open(file_name, "w")
        file.writelines(diff_commands[type])
        file.close()

    for type in clean_commands.keys():
        file_name = "%s/clean_%s.sh" % (verify_dir, type)
        file = open(file_name, "w")
        file.writelines(clean_commands[type])
        file.close()

# Entry point
main()

         

            


