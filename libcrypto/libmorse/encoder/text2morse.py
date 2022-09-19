import sounddevice as sd
import numpy as np

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

def gen_sine_wave(char):
    global S_rate
    # dit and dah duration
    t=.05 if char == '.' else .15

    # make a space character so low that only elephants can hear it
    freq = 500 if char != ' ' else 10

    S_rate=44100
    T= 1/S_rate
    N = S_rate * t
    t_seq = np.arange(N) * T
    omega = 2*np.pi*freq
    wave = np.concatenate((np.sin(omega*t_seq), np.zeros(5000)))

    return wave

def code_to_sound(code):

    wave_group=np.zeros(0)
    for char in code:
        new_wave=gen_sine_wave(char)
        wave_group=np.concatenate((wave_group, new_wave))


    return wave_group
my_message = "Merhaba Yigit"
morse_text=text_to_morse(my_message)
morse_sound=code_to_sound(morse_text)
sd.play(morse_sound, S_rate)
import time
time.sleep(55)
sd.stop()