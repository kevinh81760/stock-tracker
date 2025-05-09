# 📈 Stock Tracker Web App

This is a Flask-based web application that allows users to retrieve and view real-time stock information using the [Tiingo API](https://api.tiingo.com/). It features:

- Real-time company outlook and stock summary
- Search history tracking (via SQLite + SQLAlchemy)
- Clean tabbed interface using HTML/CSS/JS
- Live deployed version on AWS EC2

## 🌐 Live App

**🔗 http://3.133.152.84**

## 🚀 Features

- 🏢 **Company Outlook**: View metadata like company name, ticker, exchange, start date, and description
- 📊 **Stock Summary**: Real-time stock stats including last price, volume, daily high/low, change, and percent change
- 🕓 **Search History**: Displays the last 10 tickers searched
- 💾 **SQLite Database**: Saves search history and caches API results
- ⚡ **Caching**: Reduces repeated API calls (15-minute cache window)
- 📦 **Modular Flask App**: Organized by blueprints, models, and config

## 🖥 Tech Stack

- **Backend**: Flask, SQLAlchemy, requests
- **Frontend**: HTML, CSS, Vanilla JS
- **Database**: SQLite
- **API**: Tiingo API
- **Deployment**: AWS EC2 + nginx

## 📂 Project Structure
stock_tracker/
├── app.py # Main Flask app
├── config.py # API keys and Flask config
├── .env # Environment variables (not tracked)
├── requirements.txt # Python dependencies
├── README.md
│
├── db/
│ ├── init_db.py # Initializes the SQLite database
│ └── stocks.db # SQLite DB (auto-generated)
│
├── models/
│ └── models.py # SQLAlchemy models
│
├── static/
│ ├── script.js # JS fetch + tab switching logic
│ └── styles.css # Styling for layout + tables
│
├── templates/
│ └── index.html # Main HTML file
│
├── instance/ # Optional instance config
└── venv/ # Python virtual environment
