from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CachedStockData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_json = db.Column(db.Text)
    stock_json = db.Column(db.Text)
    last_update = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))