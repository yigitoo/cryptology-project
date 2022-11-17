from funcs import *
video2images('ftest.mp4')
#originsizeimgs('framesr')
for i in natsorted(os.listdir('imgsr')):
    ar = img2wavc(f'imgsr/{i}')
    write(filename=f'wavr/{i}'.replace('.png','.wav'),data=ar,rate=44100)
md = decodewavs('wavr')
print(md)
s = ""
o = ""
for i in md:
    s+=i
print(s)
for i in s.split('  '):
    o+=morse_to_text(i)+ " "
print(o)