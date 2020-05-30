<!-- markdownlint-disable single-h1 -->
<!-- markdownlint-disable first-line-h1 -->
[![Test](https://github.com/road-master/radiko_recorder/workflows/Test/badge.svg)](https://github.com/road-master/radiko_recorder/actions?query=workflow%3ATest)

# クイックリファレンス

- **参考資料**:

  [radikoを録音するpythonスクリプトを先人たちのコードを読みながら作ってわかったこと - Qiita](https://qiita.com/1021ky@github/items/0fc49fec62c6ab213e32)

<!-- markdownlint-disable no-trailing-punctuation -->
# radiko recorder とは？
<!-- markdownlint-enable no-trailing-punctuation -->

Radiko を録音する docker コンテナと python スクリプトです。

# このイメージの使い方

image をビルドして実行すると 8080 ポートで HTTP リクエストを受け付けるようになります。

例：TBS の hoge 番組を 10 分録音する場合

```console
curl '127.0.0.1:8080/record?station=TBS&program=hoge&rtime=10'
```

エリアは image ビルド時に環境変数 `RADIKO_AREA_ID` で指定されています。
必要に応じて変えてビルドします。

## 環境変数

### `RADIKO_AREA_ID`

エリア ID です。

# radiko のライブを録音する python スクリプト

## 例

東京で TBS の 番組を 10 分録音して、保存するファイル名に "hoge" の文字列を使う場合:

```console
RADIKO_AREA_ID=JP13 python src/app.py TBS hoge 10
```

# radiko のタイムフリーを録音する python スクリプト

<!-- markdownlint-disable no-duplicate-header -->
## 例
<!-- markdownlint-enable no-duplicate-header -->

東京で NACK5 の 2020 年 5 月 29 日 の21:00 ～ 23:00 の番組を録音して、
保存するファイル名に "hoge" の文字列を使う場合:

```console
RADIKO_AREA_ID=JP13 python src/time_free_app.py NACK5 hoge 20200529210000 20200529230000
```

## Author

[keisuke yamanaka](https://github.com/1012ky)
