# プロセッサシミュレーションのための環境個築スクリプト

* このリポジトリは以下を含んでいます
    * RISC-V cross compilers
    * RISC-V qemu
    * SPEC CPU 2006/2017 data/binaries
* Docker 環境を使用してクロスコンパイラや QEMU，SPEC CPU のコンパイルを行います
* 事前に Docker のインストールと，Docker が起動できるよう権限の設定を行っておいてください


## クイックスタート
* まず以下の docker-build を行ってから，Docker 環境内で各ツールのビルドを行ってください
```bash
# Docker 環境の構築
make docker-build

# Docker 環境に入る
make docker-run

# 他のディレクトリから Docker 環境に入るために launch.sh を使う事もできる
./launch.sh     

# 以下のオプションにより /dev/shm を /tmp にマウントして Docker 環境に入る
# メモリが非常にたくさんある場合，ビルドが高速に行える
SIM_ENV_USE_TMPFS=1 ./launch.sh
```

