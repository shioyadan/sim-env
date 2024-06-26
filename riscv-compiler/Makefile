#
# うまく行かない場合は，1回 disclean してやりなおす
# 特に，submodule の update が失敗しやすい
#

ifndef SIM_ENV_GCC_PREFIX_BASE
# Must specify using a absolute path
# "$(shell echo ~)" means the absolute path of a home directory
SIM_ENV_GCC_PREFIX_BASE = $(shell echo ~)/opt/gcc
endif


# ビルド時の中間ディレクトリ
TMP_PATH=/tmp/riscv-compiler

# 新しいバージョンを追加した際は，このリストにサフィックスを追加する
# 追加すると make のターゲットが自動で生成される
ALL_SRCS = 0711 0810 1110 1320

# バージョン番号とタグのリスト
GCC_VERSION_0711=7.1.1 
GCC_GIT_TAG_0711=refs/tags/v20170612 

GCC_VERSION_0810=8.1
GCC_GIT_TAG_0810=refs/tags/v20180629 

GCC_VERSION_1110=11.1
GCC_GIT_TAG_1110=refs/tags/2021.09.21

GCC_VERSION_1320=13.2
GCC_GIT_TAG_1320=refs/tags/2023.10.12

GCC_VERSION_1410=14.1
GCC_GIT_TAG_1410=refs/tags/2024.04.12

TARGET_ELF32   = $(ALL_SRCS:%=build_riscv32_elf_%)
TARGET_LINUX32 = $(ALL_SRCS:%=build_riscv32_linux_%)
TARGET_ELF64   = $(ALL_SRCS:%=build_riscv64_elf_%)
TARGET_LINUX64 = $(ALL_SRCS:%=build_riscv64_linux_%)


# elf: riscv32-unknown-elf
# ilp32: 32-bit soft-float
#   soft float をデフォルトにする場合は configure に --with-abi=ilp32 をつける

# $(patsubst build_riscv32_elf_%,%,$@) はターゲットから 711 や 81 などのバージョン番号部分を切り出している
# $(eval GCC_VERSION=$(GCC_VERSION_$(VERSION_ID))) は，VERSION_ID が 711 なら，GCC_VERSION_711 を参照する
$(TARGET_ELF32):
	$(eval VERSION_ID=$(patsubst build_riscv32_elf_%,%,$@))
	$(eval GCC_VERSION=$(GCC_VERSION_$(VERSION_ID)))
	$(eval GCC_GIT_TAG=$(GCC_GIT_TAG_$(VERSION_ID)))
	$(eval GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv32-elf/$(GCC_VERSION))
	@echo version: $(GCC_VERSION)
	@echo git: $(GCC_GIT_TAG)
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE)
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(GCC_GIT_TAG) -f ;\
		git submodule update --init --recursive -f ;\
		./configure --prefix=$(GCC_PATH) --with-arch=rv32g;\
		$(MAKE) clean ;\
		$(MAKE)

$(TARGET_LINUX32):
	$(eval VERSION_ID=$(patsubst build_riscv32_linux_%,%,$@))
	$(eval GCC_VERSION=$(GCC_VERSION_$(VERSION_ID)))
	$(eval GCC_GIT_TAG=$(GCC_GIT_TAG_$(VERSION_ID)))
	$(eval GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv32-linux/$(GCC_VERSION))
	@echo version: $(GCC_VERSION)
	@echo git: $(GCC_GIT_TAG)
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE)
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(GCC_GIT_TAG) -f ;\
		git submodule update --init --recursive -f ;\
		./configure --prefix=$(GCC_PATH) --with-arch=rv32g;\
		$(MAKE) clean ;\
		$(MAKE) linux

$(TARGET_ELF64):
	$(eval VERSION_ID=$(patsubst build_riscv64_elf_%,%,$@))
	$(eval GCC_VERSION=$(GCC_VERSION_$(VERSION_ID)))
	$(eval GCC_GIT_TAG=$(GCC_GIT_TAG_$(VERSION_ID)))
	$(eval GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv64-elf/$(GCC_VERSION))
	@echo version: $(GCC_VERSION)
	@echo git: $(GCC_GIT_TAG)
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE)
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(GCC_GIT_TAG) -f ;\
		git submodule update --init --recursive -f ;\
		./configure --prefix=$(GCC_PATH) --with-arch=rv64g;\
		$(MAKE) clean ;\
		$(MAKE)

$(TARGET_LINUX64):
	$(eval VERSION_ID=$(patsubst build_riscv64_linux_%,%,$@))
	$(eval GCC_VERSION=$(GCC_VERSION_$(VERSION_ID)))
	$(eval GCC_GIT_TAG=$(GCC_GIT_TAG_$(VERSION_ID)))
	$(eval GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv64-linux/$(GCC_VERSION))
	@echo version: $(GCC_VERSION)
	@echo git: $(GCC_GIT_TAG)
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE)
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(GCC_GIT_TAG) -f ;\
		git submodule update --init --recursive -f ;\
		./configure --prefix=$(GCC_PATH) --with-arch=rv64g;\
		$(MAKE) clean ;\
		$(MAKE) linux


build_riscv32_elf_1410:
	$(eval VERSION_ID=$(patsubst build_riscv32_elf_%,%,$@))
	$(eval GCC_VERSION=$(GCC_VERSION_$(VERSION_ID)))
	$(eval GCC_GIT_TAG=$(GCC_GIT_TAG_$(VERSION_ID)))
	$(eval GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv32-elf/$(GCC_VERSION))
	@echo version: $(GCC_VERSION)
	@echo git: $(GCC_GIT_TAG)
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE)
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(GCC_GIT_TAG) -f ;\
		git submodule update --init --recursive -f
	cd $(TMP_PATH)/riscv-gnu-toolchain/gcc ;\
		git checkout cd0059a1976 -f
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		./configure --prefix=$(GCC_PATH) --with-arch=rv32g;\
		$(MAKE) clean ;\
		$(MAKE)

build_riscv64_linux_1410:
	$(eval VERSION_ID=$(patsubst build_riscv64_linux_%,%,$@))
	$(eval GCC_VERSION=$(GCC_VERSION_$(VERSION_ID)))
	$(eval GCC_GIT_TAG=$(GCC_GIT_TAG_$(VERSION_ID)))
	$(eval GCC_PATH=$(SIM_ENV_GCC_PREFIX_BASE)/riscv64-linux/$(GCC_VERSION))
	@echo version: $(GCC_VERSION)
	@echo git: $(GCC_GIT_TAG)
	mkdir -p $(SIM_ENV_GCC_PREFIX_BASE)
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		git checkout $(GCC_GIT_TAG) -f ;\
		git submodule update --init --recursive -f
	cd $(TMP_PATH)/riscv-gnu-toolchain/gcc ;\
		git checkout cd0059a1976 -f
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		./configure --prefix=$(GCC_PATH) --with-arch=rv64g;\
		$(MAKE) clean ;\
		$(MAKE) linux

# pull --tags はリモートからのタグの取得
clone:
	mkdir $(TMP_PATH) -p
	cd $(TMP_PATH) ;\
		git clone --recursive https://github.com/riscv/riscv-gnu-toolchain
	cd $(TMP_PATH)/riscv-gnu-toolchain; \
		git pull --tags; \
		git submodule update

clean:
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		$(MAKE) distclean

distclean:
	rm $(TMP_PATH) -f -r

