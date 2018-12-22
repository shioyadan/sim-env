# RISC-V クロスコンパイラの作成スクリプト

## クイックスタート

    ```
    sudo make install_deps  # ビルドに必要なものを apt で入れる
    make clone              # gcc のコードをクローンしてくる
    
    # ビルド
    make build_riscv64_linux_7_1_1 -j8  # 7.1.1 linux
    make build_riscv64_elf_7_1_1 -j8    # 7.1.1 elf
    make build_riscv64_linux_8_1 -j8    # 8.1   linux
    make build_riscv64_elf_8_1 -j8      # 8.1   elf
    ```

## その他

* ${HOME}/opt/gcc/ 以下にインストールされるので，変更したい場合は必要に応じて make ファイルを書き換えて欲しい
* 失敗する場合は，make clean をしてからやり直す
* riscv-binutils-gdb についてなにかエラーが出た場合は，riscv-binutils-gdb を1回丸っと消して再チェックアウトすれば直ることもある
