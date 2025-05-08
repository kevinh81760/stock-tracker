from flask import Flask, render_template, request
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

@app.route('/')  
def test():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)