# SO2MarketInfoBotForDiscord

SOLD OUT 2の市場情報を取得してdiscordに流します。

## 概要

ファンタジー世界でお店を経営するゲーム「[SOLD OUT 2](https://so2.mutoys.com/)」の市場情報をDiscordに出力します。

## 使用方法

1. botを動かすためのサーバーを用意します。

1. Discordサーバーを作成します。もしくは管理者権限のあるDiscordサーバーを用意します。

1. [Discordの開発者ページ](https://discordapp.com/developers/applications/)へ行き、アプリを作成します。

1. Botアカウントを作成し、TOKENの下にあるCopyボタンをクリックし、トークンを控えます。

1. OAuth2セクションで以下の項目にチェックを入れてURLをコピーします。
    ![Image](README-IMAGE01.png)

1. そのURLを開いて、botを設置するサーバーを選択して認証します。

1. Discordの「ユーザー設定」→「テーマ」へ行き、「開発者モード」のスイッチをオンにします。

1. bot専用のチャンネルを作成します。作成したチャンネル（左部に出ているリスト群から）を右クリックして「IDをコピー」をクリックし、チャンネルIDを控えます。

1. "config.sample.ini"をREADMEに従って編集し、ファイル名を"config.ini"に変更します。

1. Python仮想環境を用意します。

    1. ```venv -p python3 venv```

    1. ```venv/bin/activate``` or ```venv\Scripts\activate```

    1. ```pip install -r requirements.txt```

1. 必要であれば"alias.sample.json"を編集して、ファイル名を"alias.json"に変更します。

1. main.pyを実行します。その後はDiscordのクライアントでコマンドを実行することができます。

## config.iniについて

config.iniは設定ファイルです。適切に編集されていないとプログラムが正常に動作しない場合がありますのでご注意ください。

### [discord]

主にDiscordまわりの設定をします。

#### token

botアカウントのトークンを記載します。

#### channel

botを反応させるチャンネルを指定します。複数指定はできません。  
チャンネルは開発者モードで得ることができるチャンネルIDで指定してください。

### [command]

コマンドを編集できます。  
市場情報を受け取るデフォルトのコマンドは```!market```ですが、設定を変更して例えば```/bazzar```にすることもできます。

#### prefix

コマンドの最初の文字を指定できます。  
デフォルトでは```!```(エクスクラメーションマーク)が指定されています。

#### market

市場情報を受け取るコマンドの文字列を指定できます。  
デフォルトでは```market```が指定されています。

#### alias

エイリアス関連のコマンドの文字列を指定できます。
デフォルトでは```alias```が指定されています。

#### shutdown

シャットダウンコマンドの文字列を指定できます。  
デフォルトでは```shutdown```が指定されています。

#### version

バージョン情報コマンドの文字列を指定できます。
デフォルトでは```version```が指定されています。

#### search

アイテム検索コマンドの文字列を指定できます。  
デフォルトでは```search```が指定されています。

#### help

ヘルプ表示コマンドの文字列を指定できます。
デフォルトでは```help```が指定されています。

#### wiki

Wikiリンク生成コマンドの文字列を指定できます。  
デフォルトでは```wiki```が指定されています。

### [misc]

その他の設定です。

#### timezone

タイムゾーンを指定できます。サーバーの所在地に関わらない時間設定が可能です。  
デフォルトでは```Asia/Tokyo```が指定されています。

#### adminsitrator

シャットダウンコマンドを実行できるユーザーのIDを指定します。  
これが設定されなかった場合、シャットダウンコマンドは正常に動作しませんのでご注意ください。

#### EnableDisplayError

エラー内容をDiscord側にも表示するかどうかを指定します。  
TrueもしくはFalseで指定してください。

## Alias.jsonについて

Alias.jsonは略称の設定ファイルです。略称や別名を登録することができます。  
編集はjsonの文法に従って行うようにしてください。左が正式名称で右が略称・別名です。  
コマンドからでも追加が可能です。

## バージョンメッセージ記述について

デフォルトでは```!version```で表示されるバージョンメッセージを、このソフトウェアを改造し配布する際に変えることを推奨します。  
その際は、開発者であるキューマン・エノビクトおよびゆずりょーの名前を「原製作者」として残すようにしてください。

## 注意点

- このプログラムの改造はMITライセンスに則る限り自由ですが、API関連を改造する場合、[API仕様ページ](https://so2-docs.mutoys.com/common/api.html)に記載されている利用条件は必ず守るようにしてください。

- APIの仕様上、ファイルを保管してから処理する方式になっています。

- APIの仕様上取得上限を定めることができないため、１ファイルの容量がかなり大きくなっています(確認できた限りでは最大で2.5MB)。直接テキストエディタで開かないことをおすすめします。

- このアプリの機能は予告なく変更される可能性があります。

## LICENSE

MIT License. See [LICENSE](LICENSE) file.
