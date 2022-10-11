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

def morse_to_text(text:str = None):
    morse_text = text.split()
    result = ""
    for char in morse_text:
        for k,v in char_to_dots.items():
            if v == char:
                result += f"{k} "
    return result[:-1]
            
            

def gen_sine_wave(char):
    global S_rate
    # dit and dah duration
    t=.5 if char == '.' else .15

    # make a space character so low that only elephants can hear it
    freq = 500 if char != ' ' else 10

    S_rate=44100
    T= 1/S_rate
    N = S_rate * t
    t_seq = np.arange(N) * T
    omega = 2*np.pi*freq
    wave = np.concatenate((np.sin(omega*t_seq), np.zeros(88200)))

    return wave

def code_to_sound(code):

    wave_group=np.zeros(0)
    for char in code:
        new_wave=gen_sine_wave(char)
        wave_group=np.concatenate((wave_group, new_wave))


    return wave_group

def input2morse(input:str = None, ignore = False):
    if ignore:
        exit
    else:
        morse_text=text_to_morse(input)
        morse_sound=code_to_sound(morse_text)
        return morse_sound


if __name__ == "__main__":
    morse_text=text_to_morse("sifre")
    morse_sound=code_to_sound(morse_text)
    np.savetxt('ms.csv',morse_sound)
    np.savetxt('msf.csv',morse_sound,'%5.6f')
    morse_sound=np.loadtxt('msf.csv')


    import sounddevice as sd
    sd.play(morse_sound, S_rate)
    import time
    time.sleep(2)
    sd.stop()
