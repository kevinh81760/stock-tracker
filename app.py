from flask import Flask, render_template, request
from config import Config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

@app.route('/')  
def test():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)