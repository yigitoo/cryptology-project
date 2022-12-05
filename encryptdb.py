from funcs import *

db = [{"telno": "0531 415 92 65",
       "kullaniciadi": "yiğitgümüş",
       "şifre": "yiğitinşifresi",
       "eposta": "yiğitgümüs@gmail.com"},
      {"telno": "0545 234 10 44",
       "kullaniciadi": "ayazgümüş",
       "şifre": "ayazınşifresi",
       "eposta": "ayazgümüs@gmail.com"}]

vk = {
    0: "tels",
    1: "pws",
    2: "ems"
}

for i in db:
    l = list(i.values())
    l2 = list(i.keys())
    ln = l[1]
    print(l)
    for j in l:
        print(j)
        ce(j, f'db/{vk[l.index(j)]}/'+j+'--'+ln +
           '.mp4', f'db/{vk[l.index(j)]}/'+j+'--'+ln)
print(db)
