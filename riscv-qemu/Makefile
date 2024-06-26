ifndef SIM_ENV_QEMU_PREFIX_BASE
# Must specify using a absolute path
# "$(shell echo ~)" means the absolute path of a home directory
SIM_ENV_QEMU_PREFIX_BASE = $(shell echo ~)/opt/qemu
endif


# ビルド時の中間ディレクトリ
TMP_PATH=/tmp/riscv-qemu

# QEMU のビルド
clone:
	wget https://download.qemu.org/qemu-9.0.1.tar.xz -P $(TMP_PATH)
	cd $(TMP_PATH); tar xJf qemu-9.0.1.tar.xz

build:
	cd $(TMP_PATH)/qemu-9.0.1; \
	./configure --prefix=$(SIM_ENV_QEMU_PREFIX_BASE)/9.0.1; \
	$(MAKE); \
	$(MAKE) install
