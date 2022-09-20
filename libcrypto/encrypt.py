import cv2 as cv
import PIL
import sys
import os
import math
import re #for checking is it a path format.


def text_cipher(string:str = None) -> str:
    # Do some crytology.
    result = ""
    return result

def text2sound(dest: str = None, output: str = None) -> str:

    return f"The video has ben decrypted in {output} path."


def sound2video(dest = None, output = None) -> str:
    return f"The sound has ben decrypted in {output} path."


def encrypter(text_dest:str = None, vidfile_out:str = None) -> str:
    if text_dest == None or text_dest == "":
        text_dest = input('Give video dest: ')
    
    elif vidfile_out == None or vidfile_out == "":
        vidfile_out = input('Give a path for text output: ')
    
    temp_sound_path = ""
    #do some os checking.
    if os.name == "nt":
        temp_sound_path = r'.\temp.wav'
        text2sound(text_dest, temp_sound_path)
        sound2video(temp_sound_path, vidfile_out)
    
    if os.name == "posix":
        temp_sound_path = r'./temp.wav'
        text2sound(text_dest, temp_sound_path)
        sound2video(temp_sound_path, vidfile_out)

    choice = input("Do you wanna see the video data?: ")
    if choice.lower() == "yes" or choice.lower() == "y":
        os.system(f'vlc {vidfile_out}')