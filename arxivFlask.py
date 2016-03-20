from flask import Flask,render_template
from flask import send_from_directory
import io
import os
import sys
app = Flask(__name__)
dirpath = os.path.join(sys.path[0],'pdf')

@app.route('/')
def hello_world():
    return app.send_static_file('arxiv.html')

if __name__ == '__main__':
    app.run()