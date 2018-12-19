#
# うまく行かない場合は，1回 disclean してやりなおす
# 特に，submodule の update が失敗しやすい
#


# Must specify using a absolute path
# "$(shell echo ~)" means the absolute path of a home directory

GCC_PREFIX_BASE = $(shell echo ~)/opt/gcc
TMP_PATH = $(shell pwd)/tmp


all:
	@echo $(GCC_PREFIX_BASE)

#
# --- 32bit
#

# elf: riscv32-unknown-elf
# ilp32: 32-bit soft-float
RISCV32_ELF_GCC_7_1_1_PATH = $(GCC_PREFIX_BASE)/riscv32-elf/7.1.1/
build_riscv32_elf_7_1_1:
	mkdir -p $(GCC_PREFIX_BASE) ;\
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout refs/tags/v20170612 -f ;\
		git submodule update --init --recursive ;\
		CFLAGS="-O2 -static" ./configure --prefix=$(RISCV32_ELF_GCC_7_1_1_PATH) --with-arch=rv32g --with-abi=ilp32 ;\
		$(MAKE)


RISCV32_ELF_GCC_8_1_PATH = $(GCC_PREFIX_BASE)/riscv32-elf/8.1
build_riscv32_elf_8_1:
	mkdir -p $(GCC_PREFIX_BASE) ;\
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout refs/tags/v20180629 -f ;\
		git submodule update --init --recursive ;\
		CFLAGS="-O2 -static" ./configure --prefix=$(RISCV32_ELF_GCC_8_1_PATH) --with-arch=rv32g --with-abi=ilp32 ;\
		$(MAKE)


RISCV32_LINUX_GCC_8_1_PATH = $(GCC_PREFIX_BASE)/riscv32-linux/8.1
build_riscv32_linux_8_1:
	mkdir -p $(GCC_PREFIX_BASE) ;\
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout refs/tags/v20180629 -f ;\
		git submodule update --init --recursive ;\
		CFLAGS="-O2 -static" ./configure --prefix=$(RISCV32_LINUX_GCC_8_1_PATH) --with-arch=rv32g ;\
		$(MAKE) linux


#
# --- 64bit
#

RISCV64_LINUX_GCC_8_1_PATH = $(GCC_PREFIX_BASE)/riscv64-linux/8.1
build_riscv64_linux_8_1:
	mkdir -p $(GCC_PREFIX_BASE) ;\
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout refs/tags/v20180629 -f ;\
		git submodule update --init --recursive ;\
		CFLAGS="-O2 -static" ./configure --prefix=$(RISCV64_LINUX_GCC_8_1_PATH) --with-arch=rv64g ;\
		$(MAKE) linux




clone:
	mkdir $(TMP_PATH) -p
	cd $(TMP_PATH) ;\
		git clone --recursive https://github.com/riscv/riscv-gnu-toolchain
	cd $(TMP_PATH)/riscv-gnu-toolchain; \
		git pull --tags;	# リモートからのタグの取得
		git submodule update

install_deps:
	# 依存のあるものをインストール
	# root で実行する
	apt install autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev


clean:
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		$(MAKE) distclean

distclean:
	rm $(GCC_PREFIX_BASE) -f -r
