# RISC-V クロスコンパイラの作成スクリプト

* Docker 環境を使用して RISC-V クロスコンパイラを生成するためのスクリプトです
    * 生成される Docker 環境は /home をマウントし，起動者の権限で起動されます
    * クロスコンパイラはデフォルトでは Docker 外の /${HOME}/opt/gcc に生成されます
* 事前に Docker のインストールと，Docker が起動できるよう権限の設定を行っておいてください


## クイックスタート

```bash
# Docker 環境の構築
make docker-build

# Docker 環境に入る
make docker-run

# 上記の Docker 環境に入ったうえで
# RISC-V gnu toolchain の clone
make clone

# GCC のビルド
# ここでは 64bit 13.2 を生成
make build_riscv64_linux_1320 -j$(nproc)

# GCC の起動
~/opt/gcc/riscv64-linux/13.2/bin/riscv64-unknown-linux-gnu-gcc
```

## その他
* デフォルトでは Docker 内の /tmp に中間ファイルやソースコードを置いてビルドする

### メモ
```bash
# 他のディレクトリから Docker 環境に入るために launch.sh を使う事もできる
./launch.sh     

# 以下のオプションにより /dev/shm を /tmp にマウントして Docker 環境に入る
# メモリが非常にたくさんある場合，ビルドが高速に行える
SIM_ENV_USE_TMPFS=1 make docker-run
```

