import numpy as np
from scipy.io.wavfile import write as write_wav
from PIL import Image
import cv2, os
import ffmpeg
import sounddevice as sd
try:
    from libcrypto.libmorse.encoder.text2morse import input2morse
    from libcrypto.libmorse.decoder.morse import MorseCode
except:
    from text2morse import input2morse
from funcs import *    


data = input('data: ')

ar = text2video(data) -1
sd.play(ar)
