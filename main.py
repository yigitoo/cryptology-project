from cipher import (
    Decrypt,
    Encrypt
)
import tkinter as tk
import threading
from functools import partial

#variables and funcs
def solver(path = None):
    Decrypt(path)
def cipher(path = None):
    Encrypt(path)

#GUI
root = tk.Tk()
frame = tk.Frame(bg='#32334f')

cipher_label = tk.Label(text = "To encypt your data give the text", fg = "#3d0192")


root.mainloop()