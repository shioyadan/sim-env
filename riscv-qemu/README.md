# QEMUの作成スクリプト

## クイックスタート

    ```
    sudo make install_deps                  # ビルドに必要なものを apt で入れる
    make clone                              # qemu のコードをクローンしてくる
    make build_qemu_linux_3_1_0 -j8       # ビルド
    make install_qemu_linux_3_1_0 -j8     # インストール
    ```

