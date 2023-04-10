from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello_world"

if __name__ == '__main__':
    app.run()