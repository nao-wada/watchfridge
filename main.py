import cv2
import os
import time
import datetime
import ftplib
##関数実行用の関数##
def main():
    photoLive_dir_path = '******/FridgePhotoLive' #冷蔵庫内の最新状況写真のみ保存用ローカルディレクトリ(FridgePhotoLive)
    photoLog_dir_path = '******/FridgePhotoLog' #冷蔵庫内の現在時刻までの過去状況写真保存用ローカルディレクトリ(FridgePhotoLog)
    photoLive_file_path = '' #33行目で説明
    photoLog_file_path = '' #34行目で説明
    betweenTime = 600 #次の処理へ移行するまでの時間(秒)
    #ローカルへの写真の保存先(FridgePhotoLive,FridgePhotoLog)を確保#
    os.makedirs(photoLive_dir_path, exist_ok = True)
    os.makedirs(photoLog_dir_path, exist_ok = True)
    #betweenTimeごとに、写真を撮影してローカルへ保存、FTPサーバへアップロードを繰り返す#
    while True:
        photoLive_file_name, photoLog_file_name, photoLive_file_path, photoLog_file_path = capturePhoto(photoLive_dir_path, photoLog_dir_path)
        uploadPhoto(photoLive_file_name, photoLog_file_name, photoLive_file_path, photoLog_file_path)
        time.sleep(betweenTime)
##写真を撮影し、ローカルへ保存処理を行う関数##
def capturePhoto(photoLive_dir_path, photoLog_dir_path):
    camera_deviceId = 0 #撮影に使用するカメラデバイスを指定
    capture = cv2.VideoCapture(camera_deviceId) #写真を撮影
    capture_times, image = capture.read() #撮影画像を取得し、画像をimageに、取得回数をcapture_timesに代入
    capture_time = datetime.datetime.now() #写真撮影をした時刻を取得
    photoLive_file_name = 'FridgePhotoLive.jpg' #FridgePhotoLiveに保存する冷蔵庫内最新状況写真のファイル名(FridgePhotoLive.jpg)
    photoLog_file_name = 'FridgePhotoLog_' + capture_time.strftime('%Y_%m%d_%H%M_%S') + ".jpg" #FridgePhotoLogに保存する冷蔵庫内状況記録用写真のファイル名(FridgePhotoLog_<年>_<月日>_<時分>_<秒>.jpg)
    photoLive_file_path = os.path.join(photoLive_dir_path, photoLive_file_name) #FridgePhotoLive.jpgのローカルファイルパス
    photoLog_file_path = os.path.join(photoLog_dir_path, photoLog_file_name) #FridgePhotoLog_<年>_<月日>_<時分>_<秒>.jpgのローカルファイルパス
    #画像の取得に成功したとき、画像をFridgePhotoLiveとFridgePhotoLogに保存する#
    if capture_times == True:
        cv2.imwrite(photoLive_file_path, image)
        cv2.imwrite(photoLog_file_path, image)
        print(capture_time.strftime('%Y年_%m月%d日_%H時%M分_%S秒') +' 画像撮影・ローカルへの保存完了')
        return photoLive_file_name, photoLog_file_name, photoLive_file_path, photoLog_file_path
        
##ローカルへ保存した写真をFTPサーバへアップロード処理を行う関数##
def uploadPhoto(photoLive_file_name, photoLog_file_name, photoLive_file_path, photoLog_file_path):
    host = '******' #FTPサーバのホスト名
    username = '******' #FTPサーバのユーザ名
    password = '******' #FTPサーバへのログインパスワード
    uploadPhoto_date = datetime.date.today() #アップロードした日付を取得
    destination_photoLive_file_path = '/FridgePhotoLive/' + photoLive_file_name #FridgePhotoLive.jpgのFTPサーバ上でのファイルパス。FTPサーバ上のFridgePhotoLiveディレクトリに保存。
    destination_photoLog_file_path = '/FridgePhotoLog/' + uploadPhoto_date.strftime('%Y年_%m月%d日') + '/' + photoLog_file_name #FridgePhotoLog_<年>_<月日>_<時分>_<秒>.jpgのFTPサーバ上でのファイルパス。FTPサーバ上のFredgePhotoLogディレクトリに保存。
    with ftplib.FTP() as ftp:
        #FTPサーバへのログイン処理#
        ftp.connect(host)
        ftp.set_pasv('True')
        ftp.login(username, password)
        #FTPサーバに、写真のアップロード先となるディレクトリ(FridgePhotoLive,FridgePhotoLog)を確保#
        if 'FridgePhotoLive' not in ftp.nlst():
            ftp.mkd('/FridgePhotoLive')
        if 'FridgePhotoLog' not in ftp.nlst():
            ftp.mkd('/FridgePhotoLog')
        if ('FridgePhotoLog/' + uploadPhoto_date.strftime('%Y年_%m月%d日')) not in ftp.nlst('FridgePhotoLog'):
            ftp.mkd('/FridgePhotoLog/' + uploadPhoto_date.strftime('%Y年_%m月%d日')) #FridgePhotoLogには撮影した日付別のフォルダを確保
        
        #FTPサーバへ写真をアップロード#
        with open(photoLive_file_path, 'rb') as fp:
            ftp.storbinary('STOR ' + destination_photoLive_file_path, fp)
        with open(photoLog_file_path, 'rb') as fp:
            ftp.storbinary('STOR ' + destination_photoLog_file_path, fp)
        print('FTPサーバへの画像アップロード完了')

if __name__ == "__main__":
    main()
