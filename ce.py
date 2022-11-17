from funcs import *
input = input('data: ')
morse_data = text_to_morse(input)
morse2wavs(morse_data)
wavs2img('wavs')
resizeimgs('imgs')
frames2video('imgs2','ftest.mp4')