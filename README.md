# jev-cli

miniから[TypeSafe Jev](https://docs.typesafe.ai/introduction)を呼ぶための小さなCLIです。Python標準ライブラリだけで動きます。

APIキーはJev CLI専用の `~/.config/jev/credentials.json` へ保存します。ディレクトリは所有者限定、ファイル権限は `0600` です。dotenvや環境変数には依存しません。

初回だけ、クリップボードのAPIキーを保存してください。キー自体は画面へ表示されません。

```bash
pbpaste | jev auth set
jev auth status
```

## 使い方

Yes/No判定は `noul` を使います。結果全体はJSON、`--value`を付けると確率だけを返します。

```bash
jev noul 'Does the message express urgency?' '本日中に直してください' --value
```

固定候補から選ぶ場合は `choice` を使います。候補は `KEY=DESCRIPTION` 形式で複数指定します。

```bash
jev choice 'Which team should handle this?' '決済連携が失敗します' \
  -o 'billing=Payment or refund issues' \
  -o 'technical=Bugs or integration failures' \
  --pretty
```

段階評価には `score` を使います。`--level` の指定順が0から始まる評価軸になります。

```bash
jev score 'How frustrated is the customer?' 'もう3日も動きません' \
  -l 'Calm' -l 'Concerned but civil' -l 'Very angry' --value
```

長文は標準入力または `@file` で渡せます。

```bash
pbpaste | jev noul 'Does this text request a refund?' --value
jev noul 'Does this document mention security risks?' @document.txt --value
```

複数質問を1回で評価する場合は、API形式のJSONを `run` へ渡します。

```bash
jev run request.json --pretty
cat request.json | jev run - --pretty
```

構造化stateには `--json-state` を付けます。

```bash
printf '%s' '{"message":"至急お願いします"}' | \
  jev noul 'Does `message` express urgency?' --json-state --value
```

## 終了コード

- `0`: 成功
- `1`: API応答またはその他のエラー
- `2`: 引数・入力エラー
- `3`: 認証エラー
- `4`: 通信、レート制限、一時的なサーバエラー

## 開発時の確認

```bash
uv run --python 3.13 -m unittest discover -s tests -v
```
