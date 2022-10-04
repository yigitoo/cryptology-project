import numpy as np
from PIL import Image
import cv2, os
import ffmpeg


def video2image():
    pass

def image2wav(image='output.png', out='output.wav'):
    img = Image.open(image)
    ar = np.asarray(img)
    ar = np.resize(ar, (ar.shape[0], ar.shape[1]))
    np.savetxt('ar1.csv',ar,'%5.6f')
    ar2 = []
    for i in ar:
        print(i)
        ar2.append(rgb2wve(i))
    np.savetxt('ar2.csv',ar2,'%5.6f')
    print(ar2[0, 0:3])
    return ar2

def wav2morse():
    pass



def rgb2wve(n):
    s = 0
    s += n[0]*256**2
    s += n[1]*256
    s += n[2]
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



try:
    from libcrypto.libmorse.encoder.text2morse import input2morse

    def text2video(text:str = None):
        from libcrypto.libmorse.encoder.text2morse import input2morse
        
        output = input2morse(text)
        return output
except:
    from text2morse import input2morse
    
def find_shape_difference(inp):
    l = inp.__len__()
    l2 = (np.ceil(np.sqrt(l)))**2
    return l2-l, int(np.sqrt(l2))

def arr2image(arr):
    fsd = find_shape_difference(arr)
    new_array = np.append(arr, ([165,16,0]*int(fsd[0])))
    new_array = new_array.reshape(fsd[1],fsd[1],3)
    return new_array

def tune(ar):
    np.savetxt('.temp.csv',ar,'%5.6f')
    ar = np.loadtxt('.temp.csv')
    ar2 = (ar+1)*10**6
    np.savetxt('.temp.csv',ar2,'%5.0f')
    ar2 = np.loadtxt('.temp.csv')
    return ar2

def savearrayasimg(ar):
    ar = np.array(ar, dtype=np.uint8)

    img = Image.fromarray(ar)
    img = img.convert('RGB')
    img.save('output.png')

def ce(text:str = None):
    ar = text2video(text)
    ar = tune(ar)
    ar = arr2rgb(ar)
    ar = arr2image(ar)
    savearrayasimg(ar)
    p2v('output.png')
    frames2video('/home/salih/cryp/cryptology-project/frames', 'cikis.mp4')


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
    print(image2wav('output.png'))
