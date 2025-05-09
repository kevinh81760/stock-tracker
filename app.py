from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from config import Config
from models.models import db, SearchHistory
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config.from_object(Config)
db.init_app(app)

api_key = Config.TIINGO_API_KEY

@app.route('/')  
def index():
    return render_template("index.html")

@app.route('/company') 
def company():
    try:
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
            return jsonify({"error": f"Invalid ticker symbol or API error: {meta_response.text}"}), 404
        company_data = meta_response.json()
        
        # stock summary
        stock_url = f"https://api.tiingo.com/iex/{ticker}"
        stock_response = requests.get(stock_url, headers=headers)
        if stock_response.status_code != 200:
            return jsonify({"error": f"Invalid ticker symbol or API error: {stock_response.text}"}), 404
        stock_data_list = stock_response.json()
        
        # bc tiingo can take in multiple parameters, we have to access the first value of the list to grab stock data
        if not stock_data_list:
            return jsonify({"error": "No stock data returned"}), 404
        stock_data = stock_data_list[0]

        # Save to search history
        with app.app_context():
            history_entry = SearchHistory(ticker=ticker)
            db.session.add(history_entry)
            db.session.commit()

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
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500
    
@app.route('/history')
def get_history():
    try:
        with app.app_context():
            # Get the 10 most recent searches
            history = SearchHistory.query.order_by(SearchHistory.timestamp.desc()).limit(10).all()
            return jsonify({
                "history": [
                    {
                        "ticker": entry.ticker,
                        "timestamp": entry.timestamp.isoformat()
                    }
                    for entry in history
                ]
            })
    except Exception as e:
        print(f"Error fetching history: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)