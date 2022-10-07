import numpy as np
from scipy.io.wavfile import write as write_wav
from PIL import Image
import cv2, os
import ffmpeg
try:
    from libcrypto.libmorse.encoder.text2morse import input2morse
    from libcrypto.libmorse.decoder.morse import MorseCode
except:
    from .text2morse import input2morse
    from ..decoder.morse import MorseCode

def text2video(text:str = None):
    output = input2morse(text)
    return output

def morse2wav(arr):
    scaled = np.int16(arr/np.max(np.abs(arr)) * 32767)
    write_wav('outt.wav', 44100, scaled)


def wav2text(file:str = None):
    try:
        decoded = MorseCode.from_wavfile(file).decode()
        sys.stdout.write(decoded + "\n")
    except UserWarning as err:
        sys.stderr.write(f"{err}\n")
        sys.exit(1)


def video2image():
    pass

def image2wav(image='output.png', out='output.wav'):
    img = Image.open(image)
    ar = np.asarray(img)
    ar = ar.flatten()
    ar2 = []
    ar3 = []
    for i in range(int(len(ar)/3)):
        nt = []
        nt.append(ar[i])
        nt.append(ar[i+1])
        nt.append(ar[i+2])
        ar2.append(nt)
    ar2 = np.array(ar2)
    for i in range(len(ar2)):
        #print(rgb2wve(ar2[i]))
        ar3.append(rgb2wve(ar2[i]))
    return ar3



def rgb2wve(n):
    s = 0
    s += int(n[0]*256**2)
    s += int(n[1]*256)
    s += int(n[2])
    return s




def wve2rgb(ln):
    n1=ln // 256 // 256 % 256
    n2=ln //256%256
    n3=ln % 256
    return np.array([n1,n2,n3])

def pa2sp(ar):
    n = ar.shape[0]
    n2 = np.ceil(np.sqrt(n))**2

    nd = n2 - n
    new_pa = np.append(pa, (15.0, 66.0, 64.0)*int(nd))
    return new_pa

def arr2rgb(arr):
    arr2 = []
    for i in range(len(arr)):
        arr2.append(wve2rgb(arr[i]*10**6))
    return arr2


def find_shape_difference(inp):
    l = inp.__len__()
    l2 = (np.ceil(np.sqrt(l)))**2
    return l2-l, int(np.sqrt(l2))


def arr2image(arr):
    fsd = find_shape_difference(arr)
    new_array = np.append(arr, ([1,1,1]*int(fsd[0])))
    new_array = new_array.reshape(fsd[1],fsd[1],3)
    return new_array

def tune(ar):
    np.savetxt('.temp.csv',ar,'%5.6f')
    ar = np.loadtxt('.temp.csv')
    ar2 = (ar+1)*10**6
    np.savetxt('.temp.csv',ar2,'%5.0f')
    ar2 = np.loadtxt('.temp.csv')
    np.savetxt('.temp2.csv',ar2,'%5.0f')

    return ar2

def savearrayasimg(ar):
    ar = np.array(ar, dtype=np.uint8)

    img = Image.fromarray(ar)
    img = img.convert('RGB')
    img.save('output.png')


def cd(inpt:str = None):
    arwv = image2wav(str)
    arwv = np.array(arwv, dtype=np.uint8)
    

def ce(text:str = None):
    ar = text2video(text)
    np.savetxt('ar.csv',ar)

    ar = tune(ar)

    ar = arr2rgb(ar)
    ar = arr2image(ar)
    savearrayasimg(ar)
    p2v('output.png')
    #frames2video('/home/salih/cryp/cryptology-project/frames', 'cikis.mp4')


def p2v(img):
    img = Image.open(img)
    img = img.convert('RGB')
    img = np.asarray(img)
    ar = np.array_split(img , int(img.shape[0]/1.0))
    ar = np.array(ar, dtype=np.uint8)
    
    for i in range(len(ar)):
        for j in range(len(ar[i])): 
            for k in range(len(ar[i][j])):
                ar2 = ar[i][j][k]
                ar2 = ar2.reshape(1,1,3)
                frame = Image.fromarray(ar2,'RGB')
                frame.save(f'/home/salih/cryp/cryptology-project/frames/{(i+1)}.png')
def frames2video(folder, out):
    video = ffmpeg.input(f'{folder}/*.png', pattern_type='glob', framerate=200)
    video = ffmpeg.output(video, out)
    ffmpeg.run(video)
    '''
        images = []
        for i in os.listdir(folder):
            global shape
            frame = cv2.imread(i)
            if i.startswith('0'):
                shape = np.asarray(i).shape
        c =  cv2.VideoWriter_fourcc(*'mp4v')
        outv = cv2.VideoWriter(out, c, 1, (shape[0], shape[1]))
        for img in images:
            outv.write(cv2.imread(os.path.join(folder, img)))
            outv.release()
    '''
if __name__ == "__main__":
    image2wav('output.png')