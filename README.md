# SO2MarketInfoBotForDiscord

SOLD OUT 2の市場情報を取得してdiscordに流します。

## 概要

ファンタジー世界でお店を経営するゲーム「[SOLD OUT 2](https://so2.mutoys.com/)」の市場情報をDiscordに出力します。

## 使用法

1. Discordサーバーを作成します。もしくは管理者権限のあるサーバーを用意します。

2. [Discordの開発者ページ](https://discordapp.com/developers/applications/)へ行き、アプリを作成します。

3. Botアカウントを作成し、TOKENの下にあるCopyボタンをクリックし、トークンを控えてください。

4. OAuth2セクションで以下の項目にチェックを入れてURLをコピーします。
    ![Image](README-IMAGE01.png)

5. そのURLを開いて、botを設置するサーバーを選択して認証します。

6. Discordの「ユーザー設定」→「テーマ」へ行き、「開発者モード」のスイッチをオンにします。

7. bot専用のチャンネルを作成します。作成したチャンネル（左部に出ているリスト群から）を右クリックして「IDをコピー」をクリックし、チャンネルIDを控えます。

8. "config.sample.ini"を基にして、"config.ini"を作成してください。

9. Python仮想環境を用意します。

    1. ```venv -p python3 venv```

    2. ```venv/bin/activate``` or ```venv\Scripts\activate```

    3. ```pip install -r requirements.txt```

10. SO2MarketInfo.pyを実行します。あとはDiscordのクライアントで```!market [商品名]```と入力するとできます。

## 注意点

- 基本的にいつAPIを叩くかは自由ですが、[API仕様](https://so2-docs.mutoys.com/common/api.html)ページに記載されている利用条件は守るようにしてください。

- APIの仕様上、ファイルを保管してから処理する方式になっています。

- APIには取得上限といった引数がないため、１ファイルの容量がかなり大きくなっています。直接テキストエディタで開かないことをおすすめします。

- このアプリの機能は予告なく変更される可能性があります。

## LICENSE

MIT License. See [LICENSE](LICENSE) file.
