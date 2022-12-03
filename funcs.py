import datetime
import numpy as np
from scipy.io.wavfile import write
from PIL import Image
import os
import ffmpeg
import cv2
from scipy.io import wavfile
from scipy.io.wavfile import write
from natsort import natsorted
import sys
import contextlib
import wave
from threading import Thread

key = []
morse_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', ' ': ' ', '0': '-----',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '&': '.-...', "'": '.----.', '@': '.--.-.', ')': '-.--.-', '(': '-.--.',
    ':': '---...', ',': '--..--', '=': '-...-', '!': '-.-.--', '.': '.-.-.-',
    '-': '-....-', '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.',
    'Ğ': '.-.--.--...', 'Ü': '.-.--.--..-', 'Ş': '.-.--.--.-.', 'Ç': '.-.--.--',
    'İ': '..-.-.-..----', '\n': '.-.-..-....--...-.', 'Ö': '-.-.--.--',
    '’': '.-.-..-....--...-.--..-', '‘': '.-.-..-....--...-.--..-',
    ';': '-..-.--.-.--.-.--'
}


def saveul(s):
    r = ""
    for i in s:
        if i.isupper() == True:
            r += "1"
        else:
            r += "0"
    return int(r, 2)


def text_to_morse(text):
    morse = []
    for i in text:
        try:
            morse.append(morse_dict[i.upper()])
        except:
            morse.append(morse_dict[i])

    return ' '.join(morse)


def morse_to_text(text: str = None):
    morse_text = text.split()
    result = ""
    for char in morse_text:
        for k, v in morse_dict.items():
            if v == char:
                result += f"{k}"
    return result


def createsound(fs, n):
    samplerate = 44100
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    data = data[0:len(data)//2]
    write(f"wavs/{n}.wav", samplerate, data.astype(np.int16))


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
            for _ in range(50000):  # pki
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


def rgb2wve(n):
    s = 0
    s += int(n[0]*256**2)
    s += int(n[1]*256)
    s += int(n[2])
    return s


def wve2rgb(ln):
    n1 = ln // 256 // 256 % 256
    n2 = ln // 256 % 256
    n3 = ln % 256
    return np.array([n1, n2, n3])


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
    s = np.random.choice(255, 3)
    new_array = np.append(arr, ([255, 0, 0]*int(fsd[0])))
    new_array = new_array.reshape(fsd[1], fsd[1], 3)
    return new_array


def savearrayasimg(ar, out):
    ar = np.array(ar, dtype=np.uint8)
    img = Image.fromarray(ar)
    img = img.convert('RGB')
    img.save(out)


def frames2video(folder, out):
    video = ffmpeg.input(f'{folder}/*.png', pattern_type='glob', framerate=60)
    video = ffmpeg.output(video, out)
    ffmpeg.run(video)


def video2images(vid):
    v = cv2.VideoCapture(vid)
    v.set(cv2.CAP_PROP_FPS, 1)
    s = 1
    c = 0
    while s:
        s, img = v.read()
        try:
            cv2.imwrite(f'framesr/{c}.png', img)
        except:
            pass
        c += 1


def get_duration(fname):
    with contextlib.closing(wave.open(fname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration


def decodewavs(folder):
    ar2 = ""
    for i in natsorted(os.listdir(folder)):
        len = get_duration(fname="".join([folder, "/", i]))
        if len >= 0.1 and len <= 0.25:
            ar2 += "."
        if len <= 0.5 and len > 0.25:
            ar2 += "-"
        if len == 1:
            ar2 += " "
    return ar2


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
    for i in natsorted(os.listdir(folder)):
        key.append(str(i[0]))
        samplerate, data = wavfile.read(os.path.join(folder, i))
        ar = arr2rgb(data)
        ar = arr2image(ar)
        savearrayasimg(ar, out=f"imgs/{i}".replace(".wav", ".png"))


def createsound(c, n):
    from scipy.io.wavfile import write
    """
    200-500 -> "."
    500-800 -> "-"
    800-1000 -> " "
    """
    k = 1
    if c == ".":
        fs = int(np.random.uniform(200, 500, (1, 1)))
        samplerate = 22050
        k = int(np.random.uniform(4, 10, (1, 1)))
    if c == "-":
        fs = int(np.random.uniform(0.5, 0.9, (1, 1)))
        samplerate = 44100
        k = int(np.random.uniform(3, 4, (1, 1)))
    if c == " ":
        fs = int(np.random.uniform(800, 1000, (1, 1)))
        samplerate = 88200
        k = 1
    samplerate = 44100
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    data = data[0:len(data)//k]
    write(f"./wavs/{n}.wav",
          samplerate, data.astype(np.int16))


def morse2wavs(data):
    for char in range(len(data)):
        if data[char] == ".":
            createsound(".", char)
        if data[char] == "-":
            createsound("-", char)
        if data[char] == " ":
            createsound(" ", char)


def unitedwavs(folder):
    ar2 = np.array([])
    for i in natsorted(os.listdir(folder)):
        sr, d = wavfile.read(os.path.join(folder, i))
        ar2 = np.append(ar2, np.append(d, 0.31415))
    write('uw.wav', data=ar2, rate=44100)
    return ar2


def resizeimgs(folder):
    list = natsorted(os.listdir(folder))
    for i in list:
        ar = np.asarray(Image.open(os.path.join(folder, i)))
        s = ar.shape
        key[list.index(i)] += str(str(s[0])+"0"+str(s[1]))
        k = 300
        ta = k**2-s[1]**2
        ar = ar.flatten()
        sa = np.array([])
        sa = np.append(sa, tuple(np.random.choice(255, 3*(ta))))
        # ar = np.append(ar, [0]*ta*3)
        ar = np.append(ar, sa)
        ar = np.array(ar, dtype=np.uint8)
        img = Image.fromarray(ar.reshape(300, 300, 3))
        img.save(f'imgs2/{i}')


def fixsize(folder):
    for i in natsorted(os.listdir(folder)):
        img = truesize(os.path.join(folder, i))
        img = Image.fromarray(img, 'RGB')
        img.save(f'imgsr/{i}')


def originsizeimgs(folder):
    for i in natsorted(os.listdir(folder)):
        indexes = []
        iar = np.asarray(Image.open(os.path.join(folder, i)))
        ar = iar.flatten()
        ar = np.split(ar, len(ar)/3)
        np.savetxt('ard0.csv', ar)
        for j in range(len(ar[0])):
            if (ar[j] == [0, 0, 0]).any():
                indexes.append(j)
        ar = np.delete(ar, indexes)
        np.savetxt('ard0.csv', ar)
        img = Image.fromarray(ar)
        img = img.convert('RGB')
        img.save(f'imgsr/{i}.png')


def truesize(img):
    ar = Image.open(img)
    ar = np.asarray(ar)
    s1 = np.floor(np.sqrt(len(ar)))
    ar = ar[0:int(s1**2)]
    return ar


def sizeviakey(folder, key):
    l = natsorted(os.listdir(folder))
    key = solvekey(key)[0]
    for i in l:
        img = Image.open(os.path.join(folder, i))
        ar = np.asarray(img).flatten()

        vfi = key[l.index(i)]
        vfis = vfi[1:]
        vfis = vfis[: int(np.ceil(len(vfis)/2))-1]
        s = [int(vfis), int(vfis), 3]
        ar = ar[: 3*int(s[0])**2]
        ar = np.array(np.array_split(ar, len(ar)/3))
        ar = ar.reshape(s)
        img = Image.fromarray(ar, 'RGB')
        img = img.convert('RGB')
        img.save(f'imgsr/{i}')


def encryptkey(key):
    ar2 = []
    for vfi in key.split('\u200d'):
        print(vfi)
        vfis = vfi[1:]
        vfis = vfis[:int(np.ceil(len(vfis)/2))-1]
        a = str(vfis) + str(np.floor(np.random.uniform(10, 99, (1, 1))[0][0]))
        ar2.append(chr(int(float(a))))
    r = ""
    for i in ar2:
        r += i
    return r


def decryptkey(key):
    ar2 = []
    for i in key:
        val = str(ord(i))
        val = val[:-2]
        c = str(key.index(i) % 10)
        c += val+"0"+val
        ar2.append(c)
    r = ""
    for i in ar2[:-1]:
        r += i+'\u200d'
    return r


def setkey(key):
    r = ""
    for i in key:
        r += i+'\u200d'
    ar2 = []
    for i in range(len(r)):
        ar2.append(str(str(r[i])))
    # for i in range(len(ar2)):
        # ar2[i] = chr(int(i))
    # r = ""
    for i in ar2:
        r += i
    # r = encryptkey(r)
    open('key', 'w+').write(r)
    return r  # +chr(saveul(open('toEncrypt.txt', 'r').read()))


def encryptkeyfile(fname):
    k = open('key', 'r')
    key = k.read()
    key = encryptkey(key)
    k = open(fname, 'w')
    k.write(key)


def solvekey(key):
    ar = key.split("\u200d")
    return ar[:-1], ar[-1]


def changeul(s, val):
    r = ""
    for i in range(len(s)):
        if val[i] == "1":
            r += s[i].upper()
        if val[i] == "0":
            r += s[i].lower()
    return r


def ce(data, outvideo):
    morse_data = text_to_morse(data)
    os.system(f'rm {outvideo}')
    morse2wavs(morse_data)
    wavs2img('wavs')
    resizeimgs('imgs')
    unitedwavs('wavs')
    frames2video('imgs2', outvideo)
    setkey(key)
    encryptkeyfile(outvideo)


def tothread(n):
    ar = img2wavc(f'imgsr/{n}')
    write(filename=f'wavr/{n}'.replace('.png', '.wav'), data=ar, rate=44100)


def cd(vid):
   # print('v2i', datetime.datetime.now())
    video2images(vid)
    dk = open('key', 'r').read()
    #print('szviakey', datetime.datetime.now())
    sizeviakey('framesr', decryptkey(dk))

    #print('forns', datetime.datetime.now())
    for i in natsorted(os.listdir('imgsr')):
        tothread(i)
        # Thread(target=tothread, args=(i,)).start()
        #print(i, 'decodewavs', datetime.datetime.now())
    md = decodewavs('wavr')

    s = ""
    o = ""
    for i in md:
        s += i
    for i in s.split('  '):
        o += morse_to_text(i) + " "
    #print('finish', datetime.datetime.now())
    print(o)
    return o


if __name__ == "__main__":
    try:
        os.system('python clear_dirs.py')
    except:
        pass
    data = open('toEncrypt.txt', 'r').read()
    if sys.argv[1] == "-c":
        os.system('python clear_dirs.py')
        ce(data, 'ftest.mp4')
    if sys.argv[1] == "-d":
        cd('ftest.mp4')
    if sys.argv[1] == "-cd":
        os.system('python clear_dirs.py')
        ce(data, 'ftest.mp4')
        cd('ftest.mp4')
