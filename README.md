# プロセッサシミュレーションのための環境個築スクリプト

* このリポジトリは以下を含んでいます
    * RISC-V cross compilers
    * RISC-V qemu
    * SPEC CPU 2006/2017 data/binaries
* Docker 環境を使用してクロスコンパイラや QEMU，SPEC CPU のコンパイルを行います
* __事前に Docker のインストールと，Docker が起動できるよう権限の設定を行っておいてく
ださい__


## クイックスタート

まず以下の docker-build を行ってから，Docker 環境内で各ツールのビルドを行ってください
```bash
# Docker 環境の構築
make docker-build

# Docker 環境に入る
make docker-run

# 他のディレクトリから Docker 環境に入るために launch.sh を使う事もできる
./launch.sh     
```

クロスコンパイラの生成と起動
```bash
# Docker 環境の構築（make docker-build）をあらかじめ済ましておく
cd riscv-compiler
../launch.sh
make clone
make build_riscv64_linux_1410 -j$(nproc)
~/opt/gcc/riscv64-linux/14.1/bin/riscv64-unknown-linux-gnu-gcc
```

QEMU の生成
```bash
cd riscv-qemu
../launch.sh
make clone 
make build  -j$(nproc)
```

その他
```bash
# 以下のオプションにより /dev/shm を /tmp にマウントして Docker 環境に入る
# メモリが非常にたくさんある場合，/tmp がメモリ上にあるためビルドが高速に行える
SIM_ENV_USE_TMPFS=1 ./launch.sh
```
## Docker 環境
* 生成される Docker 環境は /home をマウントし，起動者の権限で起動されます

## クロスコンパイラ

* クロスコンパイラはデフォルトでは Docker 外の /${HOME}/opt/gcc に生成されます
* デフォルトでは Docker 内の /tmp に中間ファイルやソースコードを置いてビルドします
* 生成されるクロスコンパイラは rv64g or rv32g をターゲットとして生成されます
    * ユーザープログラムは任意の ISA を指定できますが，libc は rv64g/rv32g によりコンパイルされたものが使用されます
* ビルドするバージョンや ISA の指定は，riscv-compiler/Makefile 内を参照して指定してください
    * ターゲットの例：
    ```bash
        # glibc rv64g 14.1
        make build_riscv64_linux_1410
        # newlib rv32g 14.1
        make build_riscv32_elf_1410
    ```

