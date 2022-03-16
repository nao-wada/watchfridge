import cv2
import os
import time
import datetime
import ftplib

def main():
    photoLive_dir_path = 'C:/Users/HTS/pythonkun/FredgePhotoLive' #最新写真のみ保存用ディレクトリ
    photoLog_dir_path = 'C:/Users/HTS/pythonkun/FredgePhotoLog' #全過去写真保存用ディレクトリ
    photoLive_file_path = ''
    photoLog_file_path = ''

    os.makedirs(photoLive_dir_path, exist_ok = True)
    os.makedirs(photoLog_dir_path, exist_ok = True)
    while True:
        photoLive_file_name, photoLog_file_name, photoLive_file_path, photoLog_file_path = capturePhoto(photoLive_dir_path, photoLog_dir_path)
        uploadPhoto(photoLive_file_name, photoLog_file_name, photoLive_file_path, photoLog_file_path)
        time.sleep(10)

def capturePhoto(photoLive_dir_path, photoLog_dir_path):
    deviceId = 0
    capture = cv2.VideoCapture(deviceId)
    capture_times, image = capture.read()
    capture_time = datetime.datetime.now()
    photoLive_file_name = 'FredgePhotoLive.jpg'
    photoLog_file_name = 'FredgePhotoLog_' + capture_time.strftime('%Y_%m%d_%H%M_%S') + ".jpg"
    photoLive_file_path = os.path.join(photoLive_dir_path, photoLive_file_name)
    photoLog_file_path = os.path.join(photoLog_dir_path, photoLog_file_name)

    if capture_times == True:
        cv2.imwrite(photoLive_file_path, image)
        cv2.imwrite(photoLog_file_path, image)
        print(capture_time.strftime('%Y年_%m月%d日_%H時%M分_%S秒') +' 撮影・保存完了')
        return photoLive_file_name, photoLog_file_name, photoLive_file_path, photoLog_file_path
        

def uploadPhoto(photoLive_file_name, photoLog_file_name, photoLive_file_path, photoLog_file_path):
    host = 'sv13114.xserver.jp'
    username = 'smartdendai@watchfridge.wdyphoto.jp'
    password = '57846903'
    uploadPhoto_date = datetime.date.today()
    destination_photoLive_file_path = '/FredgePhotoLive/' + photoLive_file_name
    destination_photoLog_file_path = '/FredgePhotoLog/' + uploadPhoto_date.strftime('%Y年_%m月%d日') + '/' + photoLog_file_name

    with ftplib.FTP() as ftp:
        ftp.connect(host)
        ftp.set_pasv('True')
        ftp.login(username, password)

        if 'FredgePhotoLive' not in ftp.nlst():
            ftp.mkd('/FredgePhotoLive')
        if 'FredgePhotoLog' not in ftp.nlst():
            ftp.mkd('/FredgePhotoLog')
        if ('FredgePhotoLog/' + uploadPhoto_date.strftime('%Y年_%m月%d日')) not in ftp.nlst('FredgePhotoLog'):
            ftp.mkd('/FredgePhotoLog/' + uploadPhoto_date.strftime('%Y年_%m月%d日'))
        with open(photoLive_file_path, 'rb') as fp:
            ftp.storbinary('STOR ' + destination_photoLive_file_path, fp)
        with open(photoLog_file_path, 'rb') as fp:
            ftp.storbinary('STOR ' + destination_photoLog_file_path, fp)
        print('アップロード完了')


if __name__ == "__main__":
    main()
