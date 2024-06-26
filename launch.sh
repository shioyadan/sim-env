#!/bin/bash
SCRIPT_DIR=$(cd $(dirname $0); pwd)
CAD_COMMAND="$@" make -f $SCRIPT_DIR/Makefile docker-run
