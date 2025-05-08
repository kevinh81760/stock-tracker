from flask import Flask, request, jsonify
import requests
from config import Config

app = Flask(__name__)

api_key = Config.TIINGO_API_KEY

@app.route('/')  
def test():
    return "Hello, World!"

@app.route('/company') 
def company():
    # grabs ticker parameter from url
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "No ticker was provided"}), 400
    
    # creates headers and url for api call
    headers = {"Authorization": f"Token {api_key}"}
    url = f"https://api.tiingo.com/tiingo/daily/{ticker}"

    response = requests.get(url, headers=headers)

    # checks validity  
    if response.status_code != 200:
        return jsonify({"error": "Invalid ticker symbol or API error"}), 404

    # dumps response from server response into data and returns a json file
    data = response.json()
    return jsonify({
        "name": data["name"],
        "ticker": data["ticker"],
        "exchangeCode": data["exchangeCode"],
        "startDate": data["startDate"],
        "description": data["description"]
    })

if __name__ == "__main__":
    app.run(debug=True)