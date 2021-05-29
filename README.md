# IoT_Frame_ops
IoTデバイスをサーバに接続するためのAPIです。<br>
RaspberryPiやM5Stackなどを接続して、ラフにIoTを実装しましょう。<br>
<br>

### AWSやGoogle Cloud、その他企業のIoTサービスとの比較
自前運用のため、転送容量や料金を気にすることありません。<br>
また、サービス終了が起こりえないので、長期間にわたりIoTを稼働することができます。<br>
具体的には、不動産や大型の機械など長期間使用するもののIoT化に役立つでしょう。<br>
<br>
このAPIはDocker上で稼働します。<br>
APIの使い方や具体的な使用例は→https://canaspad.com/post/1/
<br>

# Usage

### 動作確認のための手順
```
#このリポジトリをGit cloneする
$ git clone https://github.com/spadr/IoT_Frame_ops.git

#cdを移動
$ cd IoT_Frame_ops

#.env.exampleを.envにリネーム
$ mv .env.example .env

#app/entrypoint.shの権限変更
$ chmod +x app/entrypoint.sh

#イメージをビルドし、各コンテナを起動
$ sudo docker-compose -f docker-compose.yml up -d --build

#稼働状況を確認
$ docker-compose -f docker-compose.yml ps -a
すべてUpになっていればOKです

#ブラウザで確認
http://localhost/にアクセスして動作確認してください。
また、開発環境用にメールサーバが http://localhost/8025 で稼働していますので、
認証メールは上記URLからご確認ください。
```
### その他の操作
```
#データの初期化
$ docker-compose -f docker-compose.yml exec app python manage.py flush --no-input

#マイグレーション
$ docker-compose -f docker-compose.yml exec app python manage.py makemigrations

#DBの作成
$ docker-compose -f docker-compose.yml exec app python manage.py migrate

#静的ファイルのコピー
$ docker-compose -f docker-compose.yml exec app python manage.py collectstatic --no-input --clear

#Djangoの管理者ユーザの登録
$ docker-compose -f docker-compose.yml exec app python manage.py createsuperuser

#各コンテナを開始
$ docker-compose -f docker-compose.yml start

#各コンテナを停止
$ docker-compose -f docker-compose.yml stop

#各コンテナをリスタート
$ docker-compose -f docker-compose.yml restart

#イメージ、コンテナ、ボリューム、ネットワークを削除
$ docker-compose -f docker-compose.yml down
```
