# SO2MarketInfoBotForDiscord

SOLD OUT 2の市場情報を取得してdiscordに流します。

## 概要

ファンタジー世界でお店を経営するゲーム「[SOLD OUT 2](https://so2.mutoys.com/)」の市場情報をDiscordに出力します。

## 使用法

現時点ではこれは予定です。予告なく改変されるかもしれないしそもそも完成してないので悪しからず。

1. 適当なサーバーを用意します。
1. Discordのbotアカウントを取得します。
1. botを適当なチャンネルなどに追加します。
1. dataフォルダを作ります。
1. dataRefleshという名前がついているpyファイルを全て一回ずつ起動します。
1. dataフォルダに以下の4つのjsonファイルがあることを確認します。
    - item.json(アイテム定義)
    - rec.json(レシピ品定義)
    - sale.json(販売品)
    - req.json(注文品)
1. config.iniにbotアカウントのトークンを記述します。
1. 以下の3つのpyファイルを定期実行するよう設定します。
    - dataRefleshSaleAndReq(販売品と注文品の取得 10-15分ごと)
    - dataRefleshRec(レシピ品定義の取得 1日1回程度)
    - dataRefleshItem(アイテム定義の取得 適当。最悪手動でもいい)
1. main.pyを起動します。この時点でサービスが開始されます。

## 未定事項

- dataRefleshRecとdataRefleshItemは統合する可能性がある
- dataフォルダの作成は自動化する可能性がある
- 初回起動時のjson取得は自動化される可能性がある
- そもそも全部自動化される可能性がある(そうなったらいいね)

## 注意点

- 基本的にいつAPIを叩くかは自由ですが、[API仕様](https://so2-docs.mutoys.com/common/api.html)ページに記載されている利用条件は守るようにしてください。
- このアプリの機能は予告なく変更される可能性があります。
