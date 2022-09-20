from libcrypto.decrypt import video2sound, sound2text
from libcrypto.encrypt import text2sound, sound2video
import re

# Encrypter
class Encrypt:
    def __init__(self, destination = None, output = None) -> None:
        if destination == None or destination == "":
            while True:
                self.destination = input("Give text destination for encrypt data: ") 
                # check is it a path:
                if re.search(self.destination, '^(.+)\/([^\/]+)$'):
                    break
        elif output == None or output == "":
            while True:
                self.output = input("Give output filename to see video (just name without file_assoc): ")
        else:
            self.encrypt(destination)
    def encrypt(self, file_path = str) -> str:
        pass





# Decyrpter
class Decrypt:
    def __init__(self, destination = None, output = None) -> None:
        if destination == None or destination == "" or type(destination) != int:
            while True:
                self.destination = input("Give video destination for decyrpt to text: ") 
                # check is it a path:
                if re.search(self.destination, '^(.+)\/([^\/]+)$'):
                    break
        elif output == None or output == "":
            while True:
                self.output = input("Give output filename to see decrypted text: ")
        else:
            self.decrypt(destination)
    def decrypt(self, file_path = str) -> str:    
        pass

if __name__ == "__main__":
    print(f"Please just run the main.py for using app.")
