#
# Compiled binary files and data are copied to $(OUTPUT_DIR)/$(ARCH_PREFIX)/
#
# ATTENTION: "ext" field in $(CONFIG_FILE) must include $(ARCH_PREFIX)
#   This script extracts the most latest built files from directories
#   $(SPECCPU2006_DIR)/benchspec/CPU2006/xxxxxxx/build/<build directories>
#   that include $(ARCH_PREFIX).
#

SPECCPU2006_DIR = /work/work/cpu2006
OUTPUT_DIR      = ./data/
BUILD_CPUS = $(shell nproc)

# ARM AArch64
#CONFIG_FILE     = linux64-aarch64-gcc493.cfg
#ARCH_PREFIX     = aarch64

# x86-64
#CONFIG_FILE     = linux64-amd64-gcc472.cfg
#ARCH_PREFIX     = amd64
#CONFIG_FILE     = linux64-amd64-gcc472-debug.cfg
#ARCH_PREFIX     = amd64-debug

# Alpha
#CONFIG_FILE     = linux64-alpha-gcc453.cfg
#ARCH_PREFIX     = alpha

# RISC-V 32
# CONFIG_FILE     = linux32-riscv32-gcc81.cfg
# ARCH_PREFIX     = riscv32
# ONIKIRI2_ARCH_NAME = RISCV32Linux

# RISC-V 64
#CONFIG_FILE     = linux64-riscv64-gcc711-debug.cfg
CONFIG_FILE     = linux64-riscv64-gcc111.cfg
ARCH_PREFIX     = riscv64
ONIKIRI2_ARCH_NAME = RISCV64Linux

#CONFIG_FILE     = linux64-riscv64-gcc81.cfg
#ARCH_PREFIX     = riscv64-m64-gcc81
#ONIKIRI2_ARCH_NAME = RISCV64Linux


# Target applications. int= SPEC CPU INT, fp = SPEC CPU FP
TARGET_APPLICATIONS = int fp
#TARGET_APPLICATIONS = 453.povray
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

build:
	# Copy config file
	cp $(CONFIG_FILE) $(SPECCPU2006_DIR)/config
	cd ${SPECCPU2006_DIR}; \
		runspec --config ${CONFIG_FILE} --action runsetup --size test --ignore_errors --tune=base --define build_ncpus=$(BUILD_CPUS) $(TARGET_APPLICATIONS)
	cd ${SPECCPU2006_DIR}; \
		runspec --config ${CONFIG_FILE} --action runsetup --size train --ignore_errors --tune=base --define build_ncpus=$(BUILD_CPUS) $(TARGET_APPLICATIONS)
	cd ${SPECCPU2006_DIR}; \
		runspec --config ${CONFIG_FILE} --action runsetup --size ref --ignore_errors --tune=base --define build_ncpus=$(BUILD_CPUS) $(TARGET_APPLICATIONS)


# Extract binary files
extract_binary: 
	python3 setup_cpu2006_bin.py $(SPECCPU2006_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX)

# Extract data
extract_data:
	python3 setup_cpu2006_data.py $(SPECCPU2006_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX)

# Extract commands
extract_command:
	python3 setup_cpu2006_cmd.py $(SPECCPU2006_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX)
	python3 conv_cmd_onikiri2.py $(SPECCPU2006_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX) $(ARCH_PREFIX) $(ONIKIRI2_ARCH_NAME)

clean_spec:
	cd $(SPECCPU2006_DIR); \
		runspec --config $(CONFIG_FILE) --action clean int fp


INT_LIST = \
	400.perlbench  403.gcc  445.gobmk  458.sjeng       464.h264ref  473.astar \
	401.bzip2      429.mcf  456.hmmer  462.libquantum  471.omnetpp  483.xalancbmk \

FP_LIST = \
	410.bwaves  435.gromacs    447.dealII    459.GemsFDTD  482.sphinx3 \
	416.gamess  436.cactusADM  450.soplex    465.tonto \
	433.milc    437.leslie3d   453.povray    470.lbm \
	434.zeusmp  444.namd       454.calculix  481.wrf \

pack_binary:
	cd data/$(ARCH_PREFIX); \
		tar -cvzf ../../SPECCPU2006_INT-$(ARCH_PREFIX)-bin.tar.gz $(patsubst .%,bin/%,$(suffix $(INT_LIST)))
	cd data/$(ARCH_PREFIX); \
		tar -cvzf ../../SPECCPU2006_FP-$(ARCH_PREFIX)-bin.tar.gz $(patsubst .%,bin/%,$(suffix $(FP_LIST)))

pack_command:
	cd data/$(ARCH_PREFIX)/verify; tar -cvzf ../../../SPECCPU2006_INT-verify.tar.gz $(INT_LIST:%=*%*.sh)
	cd data/$(ARCH_PREFIX)/verify; tar -cvzf ../../../SPECCPU2006_FP-verify.tar.gz $(FP_LIST:%=*%*.sh)
	cd data/$(ARCH_PREFIX)/cmd; tar -cvzf ../../../SPECCPU2006_INT-$(ARCH_PREFIX)-cmd.tar.gz $(INT_LIST:%=*%*.json)
	cd data/$(ARCH_PREFIX)/cmd; tar -cvzf ../../../SPECCPU2006_FP-$(ARCH_PREFIX)-cmd.tar.gz $(FP_LIST:%=*%*.json)
	cd data/$(ARCH_PREFIX)/cmd.xml; tar -cvzf ../../../SPECCPU2006_INT-$(ARCH_PREFIX)-cmd-xml.tar.gz $(INT_LIST:%=*%*.xml)
	cd data/$(ARCH_PREFIX)/cmd.xml; tar -cvzf ../../../SPECCPU2006_FP-$(ARCH_PREFIX)-cmd-xml.tar.gz $(FP_LIST:%=*%*.xml)

pack_data:
	cd data/$(ARCH_PREFIX); tar -cvzf ../../SPECCPU2006_FP-run.tar.gz $(FP_LIST:%=run/%)
	cd data/$(ARCH_PREFIX); tar -cvzf ../../SPECCPU2006_INT-run.tar.gz $(INT_LIST:%=run/%)


# 事前に riscv-compiler 内で make docker-build を行い，クロスコンパイラをビルドしてください
# make docker-run で Docker 内シェルに入り，そこから SPEC の make を行って下さい
DOCKER_CONTAINER_NAME = shioyadan-sim-env-riscv-compiler
docker-run:
	docker run -ti --rm \
	-v $(PWD):/work -e USER_ID=$(shell id -u) -e GROUP_ID=$(shell id -g) \
	$(DOCKER_CONTAINER_NAME):latest 

