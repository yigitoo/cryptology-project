import numpy as np
from scipy.io.wavfile import write as write_wav
from PIL import Image
import cv2, os
import ffmpeg
import datetime 
import sys
import sounddevice as sd
import wave, struct
from scipy.io import wavfile
from scipy.io.wavfile import write
from natsort import natsorted
import librosa

try:
    from libcrypto.libmorse.encoder.text2morse import input2morse
    from libcrypto.libmorse.decoder.morse import MorseCode
except:
    from text2morse import input2morse
    #from .decoder.morse import MorseCode

def data2morse(text:str = None):
    output = input2morse(text)
    return output

#def morse2wav(arr):
#    scaled = np.int16(arr/np.max(np.abs(arr)) * 32767)
#    write_wav('outt.wav', 44100, scaled)

def createsound(fs,n):
    samplerate = 44100
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    data = data[0:len(data)//2]
    write(f"wavs/{n}.wav", samplerate, data.astype(np.int16))

def morse2wavs(data):
    for char in range(len(data)):
        if data[char] == ".":
            createsound(300,char)
        if data[char] == "-":
            createsound(600,char)
        if data[char] == " ":
            createsound(1000,char)

def morse2wav(inpt):
    ar2 = []
    for i in inpt:
        if i == ".":
            ar2.append(0)
            for _ in range(10000):
                ar2.append(0)
                ar2.append(5)
        elif i == "-":
            ar2.append(0)
            for _ in range(50000):
                ar2.append(10)
        elif i == " ":
            for _ in range(100000):
                ar2.append(20)
        else:
            return ValueError
    ar2 = np.array(ar2)
    ar2 = list(ar2)
    for i in range(len(ar2)):
        ar2[i] = [ar2[i]]*2
    return np.array(ar2, dtype=np.float32).flatten()



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

def savearrayasimg(ar, out):
    ar = np.array(ar, dtype=np.uint8)

    img = Image.fromarray(ar)
    img = img.convert('RGB')
    img.save(out)


def cd(inpt:str = None):
    arwv = image2wav(str)
    arwv = np.array(arwv, dtype=np.uint8)
    

def ce(text:str = None):
    ar = data2morse(text)
    np.savetxt('ar.csv',ar)
    ar = tune(ar)
    ar = arr2rgb(ar)
    ar = arr2image(ar)
    savearrayasimg(ar)
    p2v('ahsenegöstermekiçin.png')
    #frames2video('/home/salih/cryp/cryptology-project/frames', 'cikis.mp4')

def ce(text:str = None):
    
    ar = data2morse(text)
    np.savetxt('ar.csv',ar)
    ar = tune(ar)
    #sd.play(ar)

    ar = arr2rgb(ar)
    print('arr2rgb',datetime.datetime.now())
    ar = arr2image(ar)
    print('arr2image',datetime.datetime.now())
    savearrayasimg(ar)
    print('savearrayasimg',datetime.datetime.now())
    p2v('output.png')
    print('p2v',datetime.datetime.now())
    #frames2video('/home/salih/cryp/cryptology-project/frames', 'cikis.mp4')
    #print('frames2video',datetime.datetime.now())

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

char_to_dots = {
  'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
  'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
  'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
  'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
  'Y': '-.--', 'Z': '--..', ' ': ' ', '0': '-----',
  '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
  '6': '-....', '7': '--...', '8': '---..', '9': '----.',
  '&': '.-...', "'": '.----.', '@': '.--.-.', ')': '-.--.-', '(': '-.--.',
  ':': '---...', ',': '--..--', '=': '-...-', '!': '-.-.--', '.': '.-.-.-',
  '-': '-....-', '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.'
}

def text_to_morse(text):
    morse = [char_to_dots.get(letter.upper()) for letter in text]
    return ' '.join(morse)

def morse_to_text(text:str = None):
    morse_text = text.split()
    result = ""
    for char in morse_text:
        for k,v in char_to_dots.items():
            if v == char:
                result += f"{k} "
    return result[:-1]
            
def decodewavs(folder):
    ar2 = ""
    for i in natsorted(os.listdir(folder)):
        len = librosa.get_duration(filename=folder+"/"+i)
        if len == 0.2:
            ar2+="."
        if len == 0.5:
            ar2+="-"
        if len == 1:
            ar2+=" "
    return ar2

decodewavs('wavr')

def img2wavc(img):
    img = Image.open(img)
    img = img.convert('RGB')
    ar = np.asarray(img)
    ar2 = np.array([])
    for i in ar.flatten():
        ar2 = np.append(ar2, i)
    ar2 = np.array_split(ar2, len(ar2)/3)
    for i in range(len(ar2)):
        ar2[i] = rgb2wve(ar2[i])
    return np.array(ar2)

def wavs2img(folder):
    for i in os.listdir(folder):
        samplerate, data = wavfile.read(os.path.join(folder,i))
        ar = arr2rgb(data)
        ar = arr2image(ar)
        savearrayasimg(ar,out=f"imgs/{i}".replace(".wav",".png"))

wavs2img('wavs')


def morse2wavs(data):
    for char in range(len(data)):
    
        if data[char] == ".":
            createsound(".",char)
    
        if data[char] == "-":
            createsound("-",char)
    
        if data[char] == " ":
            createsound(" ",char)

def createsound(c,n):
    """
    200-500 -> "."
    500-800 -> "-"
    800-1000 -> " "
    """
    k = 1
    if c == ".":
        fs = int(np.random.uniform(200,500,(1,1)))
        samplerate = 22050
        k = 4
    if c == "-":
        fs = int(np.random.uniform(500,800,(1,1)))
        samplerate = 44100
        k = 2
    if c == " ":
        fs = int(np.random.uniform(800,1000,(1,1)))
        samplerate = 88200
        k = 1 
    samplerate = 44100
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    data = data[0:len(data)//k]
    write(f"wavs/{n}.wav", samplerate, data.astype(np.int16))



if __name__ == "__main__":
    image2wav('output.png')