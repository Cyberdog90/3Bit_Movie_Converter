#  ライブラリインポート
import cv2
import os
import shutil
import time
import nearly_array
import tkinter.filedialog

P = 8
#  背景ファイルの読み込み
base_img = cv2.imread("base.png", 0)
#  img配列宣言
pimg = []
#  画像読み込み
for fi in range(P):
    pimg.append(cv2.imread("./num_chip/{}.png".format(fi), 0))
#  nearly_array用の明るさリスト宣言
array = [31, 63, 95, 127, 159, 191, 223, 255]

#  変換したい動画ファイルを開く
root = tkinter.Tk()
root.withdraw()
ftype = [("file", "*")]
idir = os.path.abspath(os.path.dirname(__file__))
mfile = tkinter.filedialog.askopenfilename(filetypes=ftype, initialdir=idir)
capv = cv2.VideoCapture(mfile)


def hogeraccho(cap):
    #  前回実行時に生成されたディレクトリを削除&生成
    shutil.rmtree("./tmp/", ignore_errors=False)
    os.mkdir("./tmp/")

    #  開いた動画の総フレーム数を取得
    frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #  開いた動画のフレームレートを取得
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    #  開いた動画の横ピクセル数を取得
    cap_wid = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #  開いた動画の縦ピクセル数を取得
    cap_hei = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #  解像度タプル
    res = (int(cap_wid), int(cap_hei))

    #  1フレずつ処理
    for i in range(frame):

        #  フレーム読み込み
        ret, frame = cap.read()

        #  表示
        cv2.imshow("now convert", frame)

        #  binaryにframeデータとiを渡す
        binary(frame, i, cap_wid, cap_hei)

        #  eキーで処理を中断
        if cv2.waitKey(1) == ord("e"):
            break

    m2ovie(res, fps)


def binary(img, i, width, height):

    #  画像の縦横をP倍にする
    if height % P == 0 and width % P == 0:
        re_height = height
        re_width = width
    else:
        re_height = height + (P - (height % P))
        re_width = width + (P - (width % P))

    #  解像度を変更
    img = cv2.resize(img, (re_width, re_height),
                     interpolation=cv2.INTER_CUBIC)

    #  解像度をP分の1に変更
    img = cv2.resize(img, (int(re_width / P),
                           int(re_height / P)))

    #  モノクロ化
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    #  関数convertに処理を投げる
    convert(img_gray, i, re_width, re_height)


def convert(img, save_i, base_width, base_height):

    #  imgの縦横のピクセル数を取得
    height, width = img.shape

    #  base_imgを元画像と同じ解像度に変換
    base = cv2.resize(base_img, (base_width, base_height))

    #  画像配置
    for i in range(height):
        for j in range(width):
            pxl_col = img[i, j]
            n = int(nearly_array.near(array, pxl_col))

            base[i * P:i * P + P, j * P:j * P + P] = pimg[n]

    cv2.imwrite("./tmp/bi_output{0:05d}.png".format(save_i), base)


def m2ovie(res, fps):
    #  コーデック指定とか
    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    video = cv2.VideoWriter("video.mp4", fourcc, fps, res)

    #  フレーム数取得
    file = os.listdir("./tmp")
    count = 0
    for i in file:
        count += 1

    #  動画作成
    for i in range(1, int(count)):
        img = cv2.imread("./tmp/bi_output{0:05d}.png".format(i))
        img = cv2.resize(img, res)
        video.write(img)

    video.release()


#  時間計測開始
start = time.time()

if __name__ == "__main__":
    hogeraccho(capv)

#  時間計測終了&表示
end = time.time() - start
print("処理時間 : {}秒".format(int(end)))
