from mitcipher import (
    Decrypt,
    Encrypt
)
import tkinter as tk
import threading
from functools import partial
import pymongo as mongo


#variables and funcs
def decipher(path = None):
    Decrypt(path)
def cipher(path = None):
    Encrypt(path)

#GUI
root = tk.Tk()
root.geometry("400x400")
root.title("Kriptoloji Projesi")

frame = tk.Frame(bg='#323340')

cipher_label = tk.Label(
    frame, 
    text = "To encypt your data give the text",
    fg = "#3d0192"
)

cipher_label.grid(row=0, column=1)
frame.pack()
root.mainloop()