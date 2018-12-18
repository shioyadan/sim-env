# RISC-V クロスコンパイラの作成スクリプト

## クイックスタート
    sudo make install_deps  # ビルドに必要なものを apt で入れる
    make clone              # gcc のコードをクローンしてくる
    make -j8                # ビルド


## その他

* riscv-binutils-gdb についてなにかエラーが出た場合は，riscv-binutils-gdb を1回丸っと消して再チェックアウトすれば直る

