#
# Compiled binary files and data are copied to $(OUTPUT_DIR)/$(ARCH_PREFIX)/
#
# ATTENTION: "ext" field in $(CONFIG_FILE) must include $(ARCH_PREFIX)
#   This script extracts the most latest built files from directories
#   $(SPECCPU2006_DIR)/benchspec/CPU2006/xxxxxxx/build/<build directories>
#   that include $(ARCH_PREFIX).
#

SPECCPU2006_DIR = /home/shioya/work/gem5-work/work/benchmark/aarch64/installed/
OUTPUT_DIR      = ./data/

# ARM AArch64
#CONFIG_FILE     = linux64-aarch64-gcc493.cfg
#ARCH_PREFIX     = aarch64

# x86-64
#CONFIG_FILE     = linux64-amd64-gcc472.cfg
#ARCH_PREFIX     = amd64

# Alpha
#CONFIG_FILE     = linux64-alpha-gcc453.cfg
#ARCH_PREFIX     = alpha

# RISC-V 32
CONFIG_FILE     = linux32-riscv-gcc711.cfg
ARCH_PREFIX     = riscv32


# Target applications. int= SPEC CPU INT, fp = SPEC CPU FP
TARGET_APPLICATIONS = int fp
#TARGET_APPLICATIONS = 401.bzip2
#TARGET_APPLICATIONS = 401.bzip2 429.mcf 433.milc 444.namd 445.gobmk 453.povray 458.sjeng 462.libquantum 470.lbm 471.omnetpp

# Do not edit MAKEFILE_DIR
MAKEFILE_DIR = $(CURDIR)

# Export SPECCPU environmental variables for loading the variables from this file.
$(shell bash -c "cd ${SPECCPU2006_DIR}; source shrc; env | sed 's/=/:=/' | sed 's/^/export /' > $(MAKEFILE_DIR)/make_env.tmp")
include make_env.tmp


all: build
	#make extract_binary
	#make extract_data
	#make extract_command
	#make pack

extract: extract_binary extract_data extract_command

pack:
	cd data/$(ARCH_PREFIX); tar -cvzf ../../speccpu2006-$(ARCH_PREFIX).tar.gz *

build:
	# Copy config file
	cp $(CONFIG_FILE) $(SPECCPU2006_DIR)/config
	cd ${SPECCPU2006_DIR}; \
		runspec --config ${CONFIG_FILE} --action runsetup --size test --ignore_errors --tune=base $(TARGET_APPLICATIONS)
	cd ${SPECCPU2006_DIR}; \
		runspec --config ${CONFIG_FILE} --action runsetup --size train --ignore_errors --tune=base $(TARGET_APPLICATIONS)
	cd ${SPECCPU2006_DIR}; \
		runspec --config ${CONFIG_FILE} --action runsetup --size ref --ignore_errors --tune=base $(TARGET_APPLICATIONS)


# Extract binary files
extract_binary: 
	python3 setup_cpu2006_bin.py $(SPECCPU2006_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX)

# Extract data
extract_data:
	python3 setup_cpu2006_data.py $(SPECCPU2006_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX)

# Extract commands
extract_command:
	python3 setup_cpu2006_cmd.py $(SPECCPU2006_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX)

clean_spec:
	cd $(SPECCPU2006_DIR); \
		runspec --config $(CONFIG_FILE) --action clean int fp