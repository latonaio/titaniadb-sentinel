# titaniadb-sentinel
titaniadb-sentinelは、titaniadbを対象として、データベース監視を行うマイクロサービスです。主にエッジ上で動作します。


## Description
titaniadb-sentinelは、etcdをラップしたtitaniadbと連携します。このマイクロサービスは、titaniaが収集したデータが蓄積されたデータベースにおいて、データの置換、挿入が正しく行われるよう監視することができます。

titaniaは、IP、MACアドレス、kubernetesノードの状態、ポッドの状態など、エッジ間の安定したデータインタフェースや処理に重要なIoTメタデータをデータベースに蓄積しますが、titaniadb-sentinelは、これらのデータの置換、挿入が正しく行われるよう巡回します。
## etcd
etcdは、オープンソースで分散型のキーバリューストアです。etcdはkubernetesのプライマリーデータストアとして採用されています。
Github URL: https://github.com/etcd-io/etcd
## Input／Output
### Input
etcd(kubernetesの主要なデータストア)に保存されたデータ(Key-Value)

### Output
データベース上のデータに起きた、挿入、追加、削除、エラー等のイベントを表示します。また、etcd、MySQLのupsertを行います。

## Install
\$git clone git@bitbucket.org:latonaio/titaniadb-sentinel.git 

\$cd titaniadb_sentinel  

\$make docker-build

## File Contents
* deployment.yml  
deploymentは、PodとReplicaSetの宣言的なアップデート機能を提供するために作成されるyamlファイルです。
* etcd.py   
etcdに蓄積されたデータのkey、ID、metadataの取得や、それらのデータの挿入、追加、削除、に対するresponseを定義しています。  
Baseクラスでは、etcdにストアされたデータの監視の開始、keyの取得、挿入、削除を定義しています。
Deviceクラス、Podクラスでは、Baseクラスを継承し、それぞれDevice、Podに関するデータの操作を定義します。
* main.py  
etcd.py、mysql.py で定義された内容に従って処理を実行し、各データベースのupsertや、処理内容、エラー内容の出力を行います。
upsert_at_eventメソッドでは、eventのtypeに従って処理を行います。
* mysql.py  
MySQLへの接続、カーソルの取得、データの操作など、データベース内のデータの操作方法を定義しています。