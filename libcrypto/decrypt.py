import cv2 as cv
import PIL
import sys
import os
import math

def text_decipher(string:str = None) -> str:
    # Do some crytology.
    result = ""
    return result

def video2sound(dest = None, output = None) -> str:
    return f"The video has ben decrypted in {output} path."

def sound2text(dest = None, output = None) -> str:
    return f"The sound has ben decrypted in {output} path."

def decrypter(vid_dest:str = None, textfile_out:str = None) -> str:
    if vid_dest == None or vid_dest == "":
        vid_dest = input('Give video dest: ')
    
    elif textfile_out == None or textfile_out == "":
        textfile_out = input('Give a path for text output: ')
    
    temp_sound_path = ""
    #do some os checking.
    if os.name == "nt":
        temp_sound_path = r'.\temp.wav'
        video2sound(vid_dest, temp_sound_path)
        sound2text(temp_sound_path, textfile_out)
    
    if os.name == "posix":
        temp_sound_path = r'./temp.wav'
        video2sound(vid_dest, temp_sound_path)
        sound2text(temp_sound_path, textfile_out)

    choice = input("Do you wanna see the text file inner data?: ")
    if choice.lower() == "yes" or choice.lower() == "y":
        with open(textfile_out, 'r') as f:
            fileData = f.read()
            print(fileData)

    


if __name__ == "__main__":
    video2sound()