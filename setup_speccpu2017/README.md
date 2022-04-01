# はじめに

このディレクトリにあるスクリプトは，以下を自動的に行う

* SPECCPU 2017 のバイナリの生成と抽出
* 入力データの抽出
* バイナリの起動コマンドの生成


# 使い方

## 1. SPECCPU2017 を適当な場所にインストールする

###  1.1 SPEC2017 のisoイメージをマウント

マウントポイントを dvd とする場合
```
mkdir dvd
su
mount -t iso9660 -o loop,ro cpu2017-1_0_2.iso dvd
exit
```


###  1.2 インストール

```
cd dvd
./install.sh
```

コンパイル制御に使用する tool set の種類が表示されるので確認して Y

その後インストール先のディレクトリを入力を要求されるので入力
(ex. /home/shioya/work/cpu2017)

###  1.3 アンマウント
```
su
umount dvd
exit
```


## 2. Makefile の中の SPECCPU のインストール先などを適宜書き換える

* SPECCPU2017_DIR
    * SPEC CPU 2017 をインストールしたディレクトリを指定
* BUILD_CPUS
    * 並列コンパイルで使用する CPU 数
* OUTPUT_DIR
    * ここで指定した場所に生成済みバイナリや入力データが出力される
* CONFIG_FILE
    * SPECCPU のバイナリを生成するためのコンパイラやオプションの指定が書かれている
    * 現在は ARM AArch64, x86-64, alpha を用意しているので，適宜コメントを外して使用する
* ARCH_PREFIX 
    * バイナリをコピーするパスのプリフェイクスを指定する
    * $(OUTPUT_DIR)/$(ARCH_PREFIX)/ 以下にバイナリがコピーされる

* 設定例

    ```
    SPECCPU2017_DIR = /home/shioya/work/gem5-work/work/benchmark/aarch64/installed/
    OUTPUT_DIR      = ./data/
    BUILD_CPUS      = 8
    
    CONFIG_FILE     = linux64-aarch64-gcc493.cfg
    ARCH_PREFIX     = aarch64
    ```


## 3. SPECCPU のコンフィグファイルを適宜書き換える

* インストール・ディレクトリの config ファイルにあるファイルをコピーして編集

* アーキテクチャのビット数と，gcc のパス，ラベル名を編集
    ```
    %   define  bits        64
    %   define  gcc_dir     /usr/.

    %define label my_amd64                # (2)      Use a label meaningful to *you*.
    ```

* コンパイラのパスの変更
    * クロスコンパイラを使う場合，外部からの指定だけではなくて，ここを書き換えないとだめくさい
    ```
    %   define  gcc_dir        ~/opt/gcc/alpha/4.5.3/
    SPECLANG                = %{gcc_dir}/bin/alpha-unknown-linux-gnu-
    ```

* OPEN MP の無効化，static リンクの追加
    * LDFLAGS はリンク時に無視される & このオプションはリンク時にも使用される
    ```
    intspeed,fpspeed:
      #EXTRA_OPTIMIZE = -fopenmp -DSPEC_OPENMP
      EXTRA_OPTIMIZE = -DSPEC_SUPPRESS_OPENMP -static
    ```

* gcc のコンパイルが通らないので追加
    * inline のデフォルトの仕様が変わったせい？ で，リンクに失敗する
    * 古い仕様に戻す
        ```
        602.gcc_s,502.gcc_r:
           CPORTABILITY  = -fgnu89-inline
        ```
    * あるいは，リンク時に同じ名前のものをまとめる
        * 元から書いてある「LDCFLAGS= -z muldefs」は gcc のバージョンによっては機能しないので，以下のようにする
        ```
        LDCFLAGS        = -Xlinker -z -Xlinker muldefs -static 
        ```
    * これは LDFLAGS ではなくて，LD*C*FLAGS だが，C 以外のこれに相当するオプションが不明

## 4. make の実行

* うまういけば，OUTPUT_DIR に入力バイナリや起動コマンド，入力データが生成される
### x86-64（ホストとターゲットが同じ）の場合

* バイナリとデータの生成
    ```
    make build
    ```

* 抽出
    ```
    make extract_binary
    make extract_data
    make extract_command
    ```

* 圧縮
    ```
    make pack
    ```

### クロスコンパイラを使う場合

* 一度 x86-64 で上記を実行して，data と command を取り出しておく
    * data の生成時に，SPEC の内部で，ホストで動くプログラムがコンパイルされて使用されるため
* クロスコンパイラに切り替えて make build したあとに，make extract_bin

### 注意！

* wrf のコンパイル時に恐ろしい量のメモリが使用されるため，使用 CPU を多めにしているとメモリ不足でこけることがある
    * スワップ含めて 32GB あっても死ぬことがあった
* wrf だけ生成出来ていない場合，Makefile 内のターゲットを wrf だけにしてもう一回 make build してみるとよい


# スクリプトの説明

* setup_cpu2017_bin.py
    * コンパイル済みバイナリを集めて，指定されたディレクトリにコピーする
    
* setup_cpu2017_data.py
    * 入力データを取り出して単独で実行できるようにコピー
    
* setup_cpu2017_cmd.py
    * 各バイナリの起動コマンドが書かれた json ファイルを作成

# ビルド結果の検証

* 各実行系の出力とリファレンス出力の比較

## Onikiri/GCC 11.1/RV64G

* 環境
    * 実行系：鬼斬2 f85136f3269b45f05fb487fe8e88dc4fa8a579fc
    * ツールチェイン：gcc 11.1/RV64G  
    * データセット：test 
* 備考
    * wrf のコンパイルエラーは Ver 8 より新しいバージョンで顕在化
    * 非常に大きい関数などでジャンプの飛び先がディスプレースメントの範囲を超えると壊れる
    * Fortran に限らず gcc/g++ でも同じ事が起きる

SPEC CPU 2017 INT SPEED

| ベンチマーク名  | 番号 |   結果   | 原因                                                             | 
| --------------- | ---- | -------- | ---------------------------------------------------------------- | 
| 600.perlbench_s | 0    | 一致     | -                                                                | 
| 600.perlbench_s | 1    | 完走せず | マルチスレッド実行するコードが含まれており、onikiri のサポート外 | 
| 602.gcc_s       | 0    | 一致     | -                                                                | 
| 605.mcf_s       | 0    | 一致     | -                                                                | 
| 620.omnetpp_s   | 0    | 一致     | -                                                                | 
| 623.xalancbmk_s | 0    | 完走せず | システムコール readlinkat の引数が、onikiri のサポート外         | 
| 625.x264_s      | 0    | 一致     | -                                                                | 
| 631.deepsjeng_s | 0    | 一致     | -                                                                | 
| 641.leela_s     | 0    | 一致     | -                                                                | 
| 648.exchange2_s | 0    | 一致     | -                                                                | 
| 657.xz_s        | 0    | 一致     | -                                                                | 
| 657.xz_s        | 1    | 一致     | -                                                                | 
| 657.xz_s        | 2    | 一致     | -                                                                | 
| 657.xz_s        | 3    | 一致     | -                                                                | 
| 657.xz_s        | 4    | 一致     | -                                                                | 
| 657.xz_s        | 5    | 一致     | -                                                                | 
| 657.xz_s        | 6    | 一致     | -                                                                | 
| 657.xz_s        | 7    | 一致     | -                                                                | 
| 657.xz_s        | 8    | 一致     | -                                                                | 
| 657.xz_s        | 9    | 一致     | -                                                                | 
| 657.xz_s        | 10   | 一致     | -                                                                | 
| 657.xz_s        | 11   | 一致     | -                                                                | 

SPEC CPU 2017 FP SPEED

| ベンチマーク名  | 番号 |   結果   | 原因                                                | 
| --------------- | ---- | -------- | --------------------------------------------------- | 
| 603.bwaves_s    | 0    | 一致     | -                                                   | 
| 603.bwaves_s    | 1    | 一致     | -                                                   | 
| 607.cactuBSSN_s | 0    | 一致     | -                                                   | 
| 619.lbm_s       | 0    | 不一致   | 指数表記の 0 の数が異なる                           | 
| 621.wrf_s       | 0    | 完走せず | fotran コンパイラのバグでビルドできない             | 
| 627.cam4_s      | 0    | 不一致   | タブがスペース何個分かが異なる                      | 
| 628.pop2_s      | 0    | 不一致   | 指数表記の 0 の数と、タブがスペース何個分かが異なる | 
| 638.imagick_s   | 0    | 不一致   | 最終出力の値が小数点第7位から異なる                 | 
| 644.nab_s       | 0    | 一致     | -                                                   | 
| 649.fotonik3d_s | 0    | 一致     | -                                                   | 
| 654.roms_s      | 0    | 不一致   | 最終出力の行列の小数点第16位の値が 1 異なる         | 
