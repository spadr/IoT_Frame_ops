# Usage

### 動作確認のための手順

```
#このリポジトリをGit cloneする
$ git clone https://github.com/spadr/IoT_Frame_ops.git

#cdを移動
$ cd IoT_Frame_ops

#.env.exampleを.envにリネーム
$ mv .env.example .env

#イメージをビルドし、各コンテナを起動
$ sudo docker-compose -f docker-compose.yml up -d --build

#稼働状況を確認
$ sudo docker-compose -f docker-compose.yml ps -a
すべてUpになっていればOKです

#死活監視スクリプトの実行
$ sudo docker-compose -f docker-compose.yml exec app python manage.py alive_monitoring

```

### その他の操作

```
#データの初期化
$ sudo docker-compose -f docker-compose.yml exec app python manage.py flush --no-input

#マイグレーション
$ sudo docker-compose -f docker-compose.yml exec app python manage.py makemigrations

#DBの作成
$ sudo docker-compose -f docker-compose.yml exec app python manage.py migrate

#静的ファイルのコピー
$ sudo docker-compose -f docker-compose.yml exec app python manage.py collectstatic --no-input --clear

#Djangoの管理者ユーザの登録
$ sudo docker-compose -f docker-compose.yml exec app python manage.py createsuperuser

#イメージをビルドし、各コンテナを起動
$ sudo docker-compose -f docker-compose.yml up -d --build

#イメージ、コンテナ、ボリューム、ネットワークを削除
$ sudo docker-compose -f docker-compose.yml down

#各コンテナを開始
$ sudo docker-compose -f docker-compose.yml start

#各コンテナを停止
$ sudo docker-compose -f docker-compose.yml stop

#各コンテナをリスタート
$ sudo docker-compose -f docker-compose.yml restart

#稼働状況を確認
$ sudo docker-compose -f docker-compose.yml ps -a

#ログを確認
$ sudo docker-compose -f docker-compose.yml logs <image_name>

#コンテナ内のシェル
$ sudo docker-compose -f docker-compose.yml exec <image_name> /bin/bash
```
