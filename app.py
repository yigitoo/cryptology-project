import os
from flask import Flask, render_template, request


app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    input = request.args.get('input')
    open('toEncrypt.txt','w+').write(input)
    os.system('python funcs.py -c')
    return render_template('template.html')
