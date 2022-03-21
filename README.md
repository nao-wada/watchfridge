# プログラム
本プログラムは、「RaspberryPiに取り付けたカメラモジュールで冷蔵庫内の写真を撮影→撮影画像をRaspberryPiに保存→RaspberryPi上の画像ファイルをFTPサーバへアップロード」の過程を自動化したものである。写真撮影及びアップロード頻度は10分に1回を想定しており、ユーザにとって過度なアップロード頻度にならないように考慮した。撮影画像の保管先には、RaspberryPi側(ローカル)とサーバ側の両方にFridgePhotoLiveとFredgePhotoLogディレクトリを設ける。FridgePhotoLiveには、FridgePhotoLive.jpgファイルのみを配置し、最新画像がこのファイルに上書き保存される。一方で、FridgePhotoLogには、過去に撮影した画像をすべて保存する。FredgePhotoLiveは、WatchFredgeが最新の冷蔵庫画像を取得するための参照先として使用する。FredgePhotoLogは、AI分析に用いることを見据え、データの集積のために使用する。

# 動作環境
## Hardware (client)
* iPhone or Android
## Hardware (camera)
* Raspberry Pi Zero 2 W
* CSI Camera module
* 5V ring light
* Need Network
* FTP server
## Software (camera)
* Raspberry Pi OS Lite
* OpenCV 3.4.3
* numpy 1.21.0
