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
    
    # meta data
    meta_url = f"https://api.tiingo.com/tiingo/daily/{ticker}"
    meta_response = requests.get(meta_url, headers=headers)
    if meta_response.status_code != 200:
        return jsonify({"error": "Invalid ticker symbol or API error"}), 404
    company_data = meta_response.json()
    
    # stock summary
    stock_url = f"https://api.tiingo.com/iex/{ticker}"
    stock_response = requests.get(stock_url, headers=headers)
    if stock_response.status_code != 200:
        return jsonify({"error": "Invalid ticker symbol or API error"}), 404
    stock_data_list = stock_response.json()
    
    # bc tiingo can take in multiple parameters, we have to access the first value of the lsit to grab stock data
    if not stock_data_list:
        return jsonify({"error": "No stock data returned"}), 404
    stock_data = stock_data_list[0]

    return jsonify({
        "company": {
            "name": company_data["name"],
            "ticker": company_data["ticker"],
            "exchangeCode": company_data["exchangeCode"],
            "startDate": company_data["startDate"],
            "description": company_data["description"]
        },
        "stock": {
            "ticker": stock_data["ticker"],
            "timestamp": stock_data["timestamp"],
            "prevClose": stock_data["prevClose"],
            "open": stock_data["open"],
            "high": stock_data["high"],
            "low": stock_data["low"],
            "last": stock_data["last"],
            "volume": stock_data["volume"]
        }
    })

if __name__ == "__main__":
    app.run(debug=True)