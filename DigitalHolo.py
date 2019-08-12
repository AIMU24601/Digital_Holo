#August 2019 v1.0
#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import tkinter as tk
import tkinter.filedialog as fd
from PIL import Image, ImageTk
import numpy as np
from numpy.fft import fftshift, ifftn
import matplotlib.pyplot as plt
import cv2

d=0
distance=.25
j=20

def flag_image_pricessing(event):
    global file_name
    file_name, image = load_file()
    global image_sq
    image_sq = trimming(image,file_name)

def flag_Hologram(event):
    global theImage
    theHologram = np.array(image_sq, np.float) #numpyで処理するためndarrayに変換する
    theHologram =complex(theHologram)
    wave_length =632.8E-9
    dx =2.2E-6
    pixel =range(1,1945)
    pixel =float(pixel)

    KL = list()
    K = -1j*np.pi/wave_length/distance*(pixel**2*dx**2)
    L = -1j*np.pi/wave_length/distance*(pixel**2*dx**2)
    for i in range(1944):
        KL.append(np.exp(K[i])*np.exp(L))
    KL = np.array(KL)

    C = fftshift(ifftn(KL*theHologram))
    theImage = np.log(abs(C))

    """
    sub_window = tk.Toplevel()
    sub_window.title("Result")
    sub_window.geometry("1280x720")
    """

    display_Fourier(theImage,file_name)

def flag_figure(event):
    display_Fourier_test(theImage,file_name)

def load_file():
    #filepathをフルパスで取得
    #file_name = fd.askopenfilename(filetypes = [("Image Files", (".bmp",".jpg"))]) テスト用
    file_name = fd.askopenfilename(filetypes = [("Image Files", (".bmp"))])
    #jpgはテスト用で使うと画像がリサイズされるので注意
    #PILを使って画像を取得
    image = Image.open(file_name)
    print("load is done!")
    return file_name, image

def trimming(x,y):
    #画像をx軸で324~2268、y軸で0~1944までトリミングし保存
    imagesq = x.crop((324,0,2268,1944))
    newFile = y.replace(".bmp","_sq.png")
    imagesq.save(newFile)
    return imagesq

def display(x,y):
    #画像を表示
    photo = ImageTk.PhotoImage(y,master=x)
    tk.Label(x, image = photo).pack()

def display_Fourier(data,name):
    """
    imshow()はndarrayからの変換には対応していない模様
    plt.imshow(data, cmap="Greys")
    plt.show()
    """
    im = cv2.flip(data * j, 0)
    im = Image.fromarray(np.uint8(im))
    name = name.rstrip(".bmp")
    newfile = name + "_dist=" + str(distance) + "_Holo.png"
    im.save(newfile)
    print("save is done!")

def display_Fourier_test(data,name):
    #画像出力のテスト用です、多分使わないと思う
    name_a = name
    for i in range(50):
        im = cv2.flip(data*i, 0)
        im = Image.fromarray(np.uint8(im))
        name = name_a
        name = name.replace(".bmp","a")
        name = name.rstrip("a")
        name = name + str(i)
        newfile = name + "_Holo.png"
        im.save(newfile)

"""
photo = tk.PhotoImage(file = file_name)
tk.Label(root, image = photo).pack()
tkinter seems to be able to recognize only GIF and PGM/PPM
so we should use PIL or Pillow instead of tkinter.PhotoImage()
"""

def Enter_distance(event):
    global distance
    distance = e_1.get()
    distance = float(distance)

def Figure(event):
    global j
    j = e_2.get()
    j = int(j)

root = tk.Tk()
root.title("Digital Hologram")
root.geometry("1280x720")

lb = tk.Label(root,text="扱える画像は.bmpのみです")
lb.pack()
lb.place(x=20,y=20)

#画像選択開始用ボタン
Button_1 = tk.Button(text=u"select image")
Button_1.bind("<Button-1>",flag_image_pricessing)
Button_1.pack()
Button_1.place(x=50,y=50)

#画像選択後、処理開始用ボタン
Button_2 = tk.Button(text=u"make Hologram")
Button_2.bind("<Button-1>",flag_Hologram)
Button_2.pack()
Button_2.place(x=50,y=200)

#調整用ボタン
Button_3 = tk.Button(text=u"上手く像が現れないときはこちら")
Button_3.bind("<Button-1>",flag_figure)
Button_3.pack()
Button_3.place(x=50,y=430)

lbl_1 = tk.Label(root,text="物体からカメラの距離を入力(m)")
lbl_1.pack()
lbl_1.place(x=20,y=110)

lbl_2 = tk.Label(root,text="入力なしだと0.25(m)として計算します")
lbl_2.pack()
lbl_2.place(x=20,y=140)

lbl_3 = tk.Label(root,text="像がうまく表れないときはこちら(画像が50枚作られるので注意)")
lbl_3.pack()
lbl_3.place(x=20,y=400)

lbl_3 = tk.Label(root,text="ここに画像の末尾の数字を入力")
lbl_3.pack()
lbl_3.place(x=20,y=460)

#距離入力用
e_1 = tk.Entry(root, textvariable = d)
e_1.pack()
e_1.focus_set()
e_1.bind("<Return>", Enter_distance)
e_1.place(x=50,y=170)

e_2 = tk.Entry(root, textvariable = j)
e_2.pack()
e_2.focus_set()
e_2.bind("<Return>", Figure)
e_2.place(x=50,y=490)

"""
#画像選択用ボタンを使用しないテスト用
file_name, image = load_file()
image_sq = trimming(image,file_name)
"""

complex =np.vectorize(complex)
float = np.vectorize(float)

root.mainloop()