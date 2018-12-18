# Must specify using a absolute path
# "$(shell echo ~)" means the absolute path of a home directory
PREFIX_BASE = $(shell echo ~)/opt
TMP_PATH = $(shell pwd)/tmp

QEMU_PREFIX_BASE = $(PREFIX_BASE)/qemu


all:
	@echo $(QEMU_PREFIX_BASE)

QEMU_3_1_0_PATH = $(QEMU_PREFIX_BASE)/3.1.0/
build_qemu_linux_3_1_0:
	cd $(TMP_PATH)/qemu-3.1.0 ;\
		./configure --prefix=$(QEMU_3_1_0_PATH) ;\
		$(MAKE)

install_qemu_linux_3_1_0:
	cd $(TMP_PATH)/qemu-3.1.0 ;\
		$(MAKE) install


clone:
	mkdir $(TMP_PATH) -p
	cd $(TMP_PATH) ;\
		wget https://download.qemu.org/qemu-3.1.0.tar.xz ;\
		tar -xf qemu-3.1.0.tar.xz ;\


install_deps:
	# 依存のあるものをインストール
	# root で実行する
	apt install pkg-config libglib2.0-dev libpixman-1-dev


clean:
	cd $(TMP_PATH)/riscv-gnu-toolchain ;\
		$(MAKE) distclean

distclean:
	rm $(PREFIX_BASE) -f -r
