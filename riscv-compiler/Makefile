#
# うまく行かない場合は，1回 disclean してやりなおす
# 特に，submodule の update が失敗しやすい
#


ifndef SIM_ENV_GCC_PREFIX_BASE
# Must specify using a absolute path
# "$(shell echo ~)" means the absolute path of a home directory
SIM_ENV_GCC_PREFIX_BASE = $(shell echo ~)/opt/gcc
endif
TMP_PATH=$(shell pwd)/tmp


all:
	@echo $(SIM_ENV_GCC_PREFIX_BASE)

#
# --- 32bit ELF
#

# ELF 7.1.1
build_riscv32_elf_7_1_1:
	RISCV32_ELF_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv32-elf/7.1.1/ \
	RISCV32_ELF_GCC_TAG=refs/tags/v20170612 \
	$(MAKE) build_riscv32_elf

# ELF 8.1
build_riscv32_elf_8_1:
	RISCV32_ELF_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv32-elf/8.1/ \
	RISCV32_ELF_GCC_TAG=refs/tags/v20180629 \
	$(MAKE) build_riscv32_elf

# ELF 11.1
build_riscv32_elf_11_1:
	RISCV32_ELF_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv32-elf/11.1/ \
	RISCV32_ELF_GCC_TAG=refs/tags/2021.09.21 \
	$(MAKE) build_riscv32_elf
 
# elf: riscv32-unknown-elf
# ilp32: 32-bit soft-float
build_riscv32_elf:
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE) ;\
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(RISCV32_ELF_GCC_TAG) -f ;\
		git submodule update --init --recursive -f ;\
		CFLAGS="-O2 -static" ./configure --prefix=$(RISCV32_ELF_GCC_PATH) --with-arch=rv32g --with-abi=ilp32 ;\
		$(MAKE)


#
# --- 32bit Linux
#
# LINUX 8.1
build_riscv32_linux_8_1:
	RISCV32_LINUX_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv32-linux/8.1 \
	RISCV32_LINUX_GCC_TAG=refs/tags/v20180629 \
	$(MAKE) build_riscv32_linux

# LINUX 11.1
build_riscv32_linux_11_1:
	RISCV32_LINUX_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv32-linux/11.1 \
	RISCV32_LINUX_GCC_TAG=refs/tags/2021.09.21 \
	$(MAKE) build_riscv32_linux

build_riscv32_linux:
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE) ;\
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(RISCV32_LINUX_GCC_TAG) -f ;\
		git submodule update --init --recursive -f ;\
		CFLAGS="-O2 -static" ./configure --prefix=$(RISCV32_LINUX_GCC_PATH) --with-arch=rv32g ;\
		$(MAKE) linux


#
# --- 64bit Linux
#

# 7.1.1
build_riscv64_linux_7_1_1:
	RISCV64_LINUX_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv64-linux/7.1.1 \
	RISCV64_LINUX_GCC_TAG=refs/tags/v20170612 \
	$(MAKE) build_riscv64_linux

# 8.1
build_riscv64_linux_8_1:
	RISCV64_LINUX_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv64-linux/8.1 \
	RISCV64_LINUX_GCC_TAG=refs/tags/v20180629 \
	$(MAKE) build_riscv64_linux

# 11.1
build_riscv64_linux_11_1:
	RISCV64_LINUX_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv64-linux/11.1 \
	RISCV64_LINUX_GCC_TAG=refs/tags/2021.09.21 \
	$(MAKE) build_riscv64_linux

build_riscv64_linux:
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE) ;\
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(RISCV64_LINUX_GCC_TAG) -f ;\
		git submodule update --init --recursive -f;\
		CFLAGS="-O2 -static" ./configure --prefix=$(RISCV64_LINUX_GCC_PATH) --with-arch=rv64g ;\
		$(MAKE) linux

#
# --- 64bit ELF
#

# 7.1.1
build_riscv64_elf_7_1_1:
	RISCV64_ELF_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv64-elf/7.1.1 \
	RISCV64_ELF_GCC_TAG=refs/tags/v20170612 \
	$(MAKE) build_riscv64_elf

# 8.1
build_riscv64_elf_8_1:
	RISCV64_ELF_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv64-elf/8.1 \
	RISCV64_ELF_GCC_TAG=refs/tags/v20180629 \
	$(MAKE) build_riscv64_elf

# 11.1
build_riscv64_elf_11_1:
	RISCV64_ELF_GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv64-elf/11.1 \
	RISCV64_ELF_GCC_TAG=refs/tags/2021.09.21 \
	$(MAKE) build_riscv64_elf

build_riscv64_elf:
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE) ;\
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(RISCV64_ELF_GCC_TAG) -f ;\
		git submodule update --init --recursive -f ;\
		CFLAGS="-O2 -static" ./configure --prefix=$(RISCV64_ELF_GCC_PATH) --with-arch=rv64g ;\
		$(MAKE)

# pull --tags はリモートからのタグの取得
clone:
	mkdir $(TMP_PATH) -p
	cd $(TMP_PATH) ;\
		git clone --recursive https://github.com/riscv/riscv-gnu-toolchain
	cd $(TMP_PATH)/riscv-gnu-toolchain; \
		git pull --tags; \
		git submodule update

clone_shallow:
	mkdir $(TMP_PATH) -p
	cd $(TMP_PATH) ;\
		git clone --depth 1 --single-branch -b v20180629 https://github.com/riscv/riscv-gnu-toolchain
	cd $(TMP_PATH)/riscv-gnu-toolchain; \
		git submodule update --init --recursive --recommend-shallow --depth 1 

# 依存のあるものをインストール
# root で実行する
install_deps:
	apt install autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev


clean:
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		$(MAKE) distclean

distclean:
	rm $(TMP_PATH) -f -r



# make docker-build で Docker の初期化を行います
# クロスコンパイラをビルドし，Docker 内の /opt にインストールします
#
# make docker-run で，ホストのカレントディレクトリを Docker 内の /work にマウントして 
# Docker を起動します
USER_NAME = $(shell whoami)

# Docker コンテナ名
DOCKER_CONTAINER_NAME = shioyadan-sim-env-riscv-compiler

# Docker コマンド
# ホストのカレントディレクトリを /work にマウント
# 起動したユーザーの ID でアクセスできるように外部から渡している
DOCKER_COMMAND = \
	docker run -ti --rm \
	-v $(PWD):/work -e USER_ID=$(shell id -u) -e GROUP_ID=$(shell id -g) \
	$(DOCKER_CONTAINER_NAME):latest 

# Docker コンテナを初期化
docker-build:
	docker build -t $(DOCKER_CONTAINER_NAME) .

# Docker 内シェルに入る
docker-run:
	$(DOCKER_COMMAND) 

# Docker 外から gcc を直接起動
docker-test-version:
	$(DOCKER_COMMAND) /usr/local/gcc/riscv64-linux/11.1/bin/riscv64-unknown-linux-gnu-gcc --version

docker-test-compile:
	$(DOCKER_COMMAND) /usr/local/gcc/riscv64-linux/11.1/bin/riscv64-unknown-linux-gnu-gcc test.c -static

# 使用する際は事前に docker グループに自身を追加しておいてください
docker-add-user:
	gpasswd -a $(USER_NAME) docker
