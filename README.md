# IoT_Frame_ops
IoTデバイスをサーバに接続するためのAPIです<br>
自前運用のため、転送容量や料金を気にすることなく、IoTを実装できます。<br>
Docker上で稼働するため、様々な環境やサーバでお使いになれます。<br>
HTTPで通信を行うので、煩雑な設定や証明書が必要ありません。また、IoTデバイスのコードも簡潔になります。<br>
セキュリティを担保したい場合は、IoTデバイス上でデータを暗号化し、お手元で復号する方法があります。<br>
<br>
# Usage
```
#イメージをビルドし、各コンテナを起動
$ docker-compose -f docker-compose.yml up -d --build

#稼働状況を確認
$ docker-compose -f docker-compose.yml ps -a

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

#各コンテナを一時停止
$ docker-compose -f docker-compose.yml start

#各コンテナを停止
$ docker-compose -f docker-compose.yml stop

#各コンテナをリスタート
$ docker-compose -f docker-compose.yml restart

#イメージ、コンテナ、ボリューム、ネットワークを削除
$ docker-compose -f docker-compose.yml down
```
