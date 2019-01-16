# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0303,C0326,R0201,R0903

import re
import argparse
import sys
import os

import json
import xml.etree.ElementTree as ET

def make_directory(path):
    """ Create a directory if there is not a specified directory """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def dictionary_to_node(dic):
    """ Convert a dictionary to a tree for ElementTree. """
        
    def to_element(tag, dic):
        """ Convert a dictionary to a element node. """
        node = ET.Element(tag)
        node.tail = "\n"
        for child in dic:
            if child[0] == "@":
                name = child[1:]
                node.attrib[name] = dic[child]
            else:
                for i in dic[child]:
                    node.append(to_element(child, i))
        return node
        
    if len(dic) != 1:
        print("Dictionary data has no root node or multiple root nodes.")
        return None

    root = list(dic.keys())
    root_tag = root[0]
    return to_element(root_tag, dic[root_tag])


def convert_files(dst_cmd_dir, src_cmd_dir, arch_prefix, onikiri2_arch_name):
    """ Enumerate source command files """

    if not os.path.isdir(src_cmd_dir):
        print("Error: '%s' seems not to be generated." % (src_cmd_dir))
        return ""

    for i in os.listdir(src_cmd_dir):
        if not re.search(r"\.json", i):
            continue        # not json file
        
        #print(i)

        file = open(src_cmd_dir + "/" + i, "rt")
        json_data = json.load(file)
        file.close()

        process = json_data["session"]["processes"]["process"]
        args = ""
        for a in process["args"]:
            args += a + " "
        xml_data = {
            "Session": {
                "Emulator": [{
                    "@TargetArchitecture": onikiri2_arch_name,
                    "Processes": [{
                        "Process": [{
                            # In onikiri, an upper directory must be specified
                            # due to the difference of data structure
                            "@TargetBasePath": "../../",
                            "@TargetWorkPath":  re.sub(r"^\.\./", "", process["work"]), 
                            "@Command":         arch_prefix + "/" + re.sub(r"^\.\./", "", process["bin"]),
                            "@CommandArguments": args,
                            "@STDIN": process["stdin"],
                            "@STDOUT": process["stdout"],
                            "@STDERR": process["stderr"],
                        }]
                    }]
                }]
            }
        }
        element_root = dictionary_to_node(xml_data)
        tree = ET.ElementTree(element_root)

        dst_file_name = dst_cmd_dir + "/" + re.sub(r"\.json$", ".xml", i)

        tree.write(
            dst_file_name, 
            encoding="utf-8", 
            xml_declaration='<?xml version="1.0" encoding="utf-8" ?>\n',
            method="xml"
        )


    
def main():
    """ main rountine """

    # Parse arguments 
    parser = argparse.ArgumentParser(description='SPECCPU2017 command converter for Onikiri2.')
    parser.add_argument('INSTALL_DIR', type=str, help='Specify a SEPCCPU2017 directory.')
    parser.add_argument('OUTPUT_DIR', type=str, help='Specify a destination directory.')
    parser.add_argument('ARCH_PREFIX', type=str, help='Specify an architecure name prefix. This script will output data to data/$(ARCH_PREFIX)')
    parser.add_argument('MARKER', type=str, 
        help='Specify an architectural name maker. This script search files from benchspec/CPU2017/xxx/run/* including this mark')
    parser.add_argument('ONIKIRI2_ARCH_NAME', type=str, 
        help='Specify an architectural name such as AlphaLinux and RISCV64Linux')
    args = parser.parse_args()

    #marker = args.MARKER
    arch_prefix = args.ARCH_PREFIX
    onikiri2_arch_name = args.ONIKIRI2_ARCH_NAME
    src_dir = args.OUTPUT_DIR + "/" + arch_prefix + "/cmd"
    dst_dir = args.OUTPUT_DIR + "/" + arch_prefix + "/cmd.xml"

    make_directory(dst_dir)

    convert_files(dst_dir, src_dir, arch_prefix, onikiri2_arch_name)

main()
