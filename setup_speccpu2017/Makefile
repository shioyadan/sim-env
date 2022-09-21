#
# Compiled binary files and data are copied to $(OUTPUT_DIR)/$(ARCH_PREFIX)/
#
# ATTENTION: "ext" field in $(CONFIG_FILE) must include $(ARCH_PREFIX)
#   This script extracts the most latest built files from directories
#   $(SPECCPU2006_DIR)/benchspec/CPU2006/xxxxxxx/build/<build directories>
#   that include $(ARCH_PREFIX).
#

SPECCPU2017_DIR = /work/work/cpu2017
OUTPUT_DIR      = ./data/
BUILD_CPUS = $(shell nproc)


# ARM AArch64
#CONFIG_FILE     = linux64-aarch64-gcc493.cfg
#ARCH_PREFIX     = aarch64
#MY_MARKER       = my_aarch64  # is defined as "label" in the cfg file

# x86-64
#CONFIG_FILE     = linux64-amd64-gcc472.cfg
#ARCH_PREFIX     = amd64
#MY_MARKER       = my_amd64  # is defined as "label" in the cfg file

# Alpha
#CONFIG_FILE     = linux64-alpha-gcc453.cfg
#ARCH_PREFIX     = alpha
#MY_MARKER       = my_alpha  # is defined as "label" in the cfg file

# RISC-V 32
#CONFIG_FILE     = linux32-riscv-gcc711.cfg
#ARCH_PREFIX     = riscv32
#MY_MARKER       = my_riscv32  # is defined as "label" in the cfg file

# RISC-V 64 Debug
#CONFIG_FILE     = linux64-riscv64-gcc711-debug.cfg
#ARCH_PREFIX     = riscv64-debug
#MY_MARKER       = my_riscv64_debug  # is defined as "label" in the cfg file

# RISC-V 64
#CONFIG_FILE     = linux64-riscv64-gcc711.cfg
#ARCH_PREFIX     = riscv64
#MY_MARKER       = my_riscv64  # is defined as "label" in the cfg file

# 8.1 は以下のパッチを自力で当てる必要がある
# https://patchwork.ozlabs.org/patch/1036036/
# CONFIG_FILE     = linux64-riscv64-gcc81.cfg
# ARCH_PREFIX     = riscv64
# MY_MARKER       = my_riscv64_81  # is defined as "label" in the cfg file

CONFIG_FILE     = linux64-riscv64-gcc111.cfg
ARCH_PREFIX     = riscv64
MY_MARKER       = my_riscv64_111  # is defined as "label" in the cfg file

ONIKIRI2_ARCH_NAME = RISCV64Linux


# Target applications. intspeed= SPEC CPU INT Speed, fpspeed = SPEC CPU FP Speed
TARGET_APPLICATIONS = intspeed fpspeed
#TARGET_APPLICATIONS = 602.gcc_s
#TARGET_APPLICATIONS = 621.wrf_s
#TARGET_APPLICATIONS = 600.perlbench_s
#TARGET_APPLICATIONS = 603.bwaves_s 657.xz_s

# Do not edit MAKEFILE_DIR
MAKEFILE_DIR = $(CURDIR)

# Export SPECCPU environmental variables for loading the variables from this file.
$(shell bash -c "cd ${SPECCPU2017_DIR}; source shrc; env | sed 's/=/:=/' | sed 's/^/export /' > $(MAKEFILE_DIR)/make_env.tmp")
include make_env.tmp


all: build
	#make extract_binary
	#make extract_data
	#make extract_command
	#make pack

extract: extract_binary extract_data extract_command


build:
	# Copy config file
	cp $(CONFIG_FILE) $(SPECCPU2017_DIR)/config
	cd ${SPECCPU2017_DIR}; \
		runcpu --config ${CONFIG_FILE} --action runsetup --size test,train,refspeed \
		--ignore_errors --tune=base $(TARGET_APPLICATIONS) \
		--define build_ncpus=$(BUILD_CPUS) 

run_test:
	cd ${SPECCPU2017_DIR}; \
		runcpu --config ${CONFIG_FILE} --action run --size test $(TARGET_APPLICATIONS


# Extract binary files
extract_binary: 
	python3 setup_cpu2017_bin.py $(SPECCPU2017_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX) $(MY_MARKER)

# Extract data
extract_data:
	python3 setup_cpu2017_data.py $(SPECCPU2017_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX) $(MY_MARKER)

# Extract commands
extract_command:
	python3 setup_cpu2017_cmd.py $(SPECCPU2017_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX) $(MY_MARKER)
	python3 conv_cmd_onikiri2.py $(SPECCPU2017_DIR) $(OUTPUT_DIR) $(ARCH_PREFIX) $(MY_MARKER) $(ONIKIRI2_ARCH_NAME)

# Verify input data
verify_input_data:
	cd $(OUTPUT_DIR)/$(ARCH_PREFIX)/cmd; ./verify_input_refspeed.sh
	cd $(OUTPUT_DIR)/$(ARCH_PREFIX)/cmd; ./verify_input_test.sh
	cd $(OUTPUT_DIR)/$(ARCH_PREFIX)/cmd; ./verify_input_train.sh


clean_spec:
	cd $(SPECCPU2017_DIR); \
		runcpu --config $(CONFIG_FILE) --action realclean intspeed fpspeed

INT_LIST = \
	600.perlbench_s 602.gcc_s 620.omnetpp_s 648.exchange2_s \
	631.deepsjeng_s 605.mcf_s 623.xalancbmk_s 625.x264_s \
	641.leela_s     657.xz_s

FP_LIST = \
	619.lbm_s    627.cam4_s 644.nab_s       628.pop2_s \
	603.bwaves_s 621.wrf_s  649.fotonik3d_s 638.imagick_s \
	654.roms_s   607.cactuBSSN_s 

pack_binary:
	cd data/$(ARCH_PREFIX); \
		tar -cvzf ../../SPECCPU2017_INT_SPEED-$(ARCH_PREFIX)-bin.tar.gz $(patsubst .%,bin/%,$(suffix $(INT_LIST)))
	cd data/$(ARCH_PREFIX); \
		tar -cvzf ../../SPECCPU2017_FP_SPEED-$(ARCH_PREFIX)-bin.tar.gz $(patsubst .%,bin/%,$(suffix $(FP_LIST)))

pack_command:
	cd data/$(ARCH_PREFIX)/cmd; tar -cvzf ../../../SPECCPU2017_INT_SPEED-verify.tar.gz $(INT_LIST:%=*%*.sh)
	cd data/$(ARCH_PREFIX)/cmd; tar -cvzf ../../../SPECCPU2017_FP_SPEED-verify.tar.gz $(FP_LIST:%=*%*.sh)
	cd data/$(ARCH_PREFIX)/cmd; tar -cvzf ../../../SPECCPU2017_INT_SPEED-$(ARCH_PREFIX)-cmd.tar.gz $(INT_LIST:%=*%*.json)
	cd data/$(ARCH_PREFIX)/cmd; tar -cvzf ../../../SPECCPU2017_FP_SPEED-$(ARCH_PREFIX)-cmd.tar.gz $(FP_LIST:%=*%*.json)
	cd data/$(ARCH_PREFIX)/cmd.xml; tar -cvzf ../../../SPECCPU2017_INT_SPEED-$(ARCH_PREFIX)-cmd-xml.tar.gz $(INT_LIST:%=*%*.xml)
	cd data/$(ARCH_PREFIX)/cmd.xml; tar -cvzf ../../../SPECCPU2017_FP_SPEED-$(ARCH_PREFIX)-cmd-xml.tar.gz $(FP_LIST:%=*%*.xml)

pack_data:
	cd data/$(ARCH_PREFIX); tar -cvzf ../../SPECCPU2017_FP_SPEED-run.tar.gz $(FP_LIST:%=run/%)
	cd data/$(ARCH_PREFIX); tar -cvzf ../../SPECCPU2017_INT_SPEED-run.tar.gz $(INT_LIST:%=run/%)


# 事前に riscv-compiler 内で make docker-build を行い，クロスコンパイラをビルドしてください
# make docker-run で Docker 内シェルに入り，そこから SPEC の make を行って下さい
DOCKER_CONTAINER_NAME = shioyadan-sim-env-riscv-compiler
docker-run:
	docker run -ti --rm \
	-v $(PWD):/work -e USER_ID=$(shell id -u) -e GROUP_ID=$(shell id -g) \
	$(DOCKER_CONTAINER_NAME):latest 

