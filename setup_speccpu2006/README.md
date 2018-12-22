# はじめに

このディレクトリにあるスクリプトは，以下を自動的に行う

* SPECCPU 2006 のバイナリの生成と抽出
* 入力データの抽出
* バイナリの起動コマンドの生成


# 使い方

## 1. SPECCPU2006 を適当な場所にインストールする

###  1.1 SPEC2006 のisoイメージをマウント

マウントポイントを dvd とする場合

    mkdir dvd
    su
    mount -t iso9660 -o loop,ro CPU2006v1.0.1.ISO dvd
    exit


###  1.2 インストール

    cd dvd
    ./install.sh

コンパイル制御に使用する tool set の種類が表示されるので確認して Y

その後インストール先のディレクトリを入力を要求されるので入力
(ex. /home/ichi-h/work/cpu2006)

###  1.3 アンマウント
    su
    umount dvd
    exit


## 2. Makefile の中の SPECCPU のインストール先などを適宜書き換える

* OUTPUT_DIR
    * ここで指定した場所に生成済みバイナリや入力データが出力される
* CONFIG_FILE
    * SPECCPU のバイナリを生成するためのコンパイラやオプションの指定が書かれている
    * 現在は ARM AArch64, x86-64, alpha を用意しているので，適宜コメントを外して使用する
* ARCH_PREFIX 
    * バイナリをコピーするパスのプリフェイクスを指定する
    * $(OUTPUT_DIR)/$(ARCH_PREFIX)/ 以下にバイナリがコピーされる

* 設定例

    SPECCPU2006_DIR = /home/shioya/work/gem5-work/work/benchmark/aarch64/installed/
    OUTPUT_DIR      = ./data/
    CONFIG_FILE     = linux64-aarch64-gcc493.cfg
    ARCH_PREFIX     = aarch64
    
## 3. SPECCPU のコンフィグファイルを適宜書き換える（たとえば linux64-aarch64-gcc493.cfg）

* GCC/G++/GFORTRAN の項目は書き換えが必須
    * クロスコンパイラをインストールしたパスを指定
    CC           = gcc
    CXX          = g++
    FC           = gfortran


* 互換性等のために以下の設定も追加
    
    # 並列 make を行うためのオプション
    makeflags = -j
    
    # 起動時に SPEC の最新版
    check_version = no

    # DealII は，必要な stddef.h を include してないので追加
    447.dealII=default=default=default:
    CXXPORTABILITY= -include stddef.h
    
    # static リンクするためのオプションを追加
    LDPORTABILITY = -static


    
## 4. make の実行
    * うまういけば，OUTPUT_DIR に入力バイナリや起動コマンド，入力データが生成される



# スクリプト説明
* setup_cpu2006_bin.py
    * コンパイル済みバイナリを集めて，指定されたディレクトリにコピーする
    
* setup_cpu2006_data.py
    * インストール済みディレクトリから，SPECCPU2006 の入力データを取り出して単独で実行できるようにコピー
    
* setup_cpu2006_cmd.py
    * 各バイナリの起動コマンドが書かれた json ファイルを作成

