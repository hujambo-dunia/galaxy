import requests
import jmespath
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///galaxy_instances.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Instance(db.Model):
    __tablename__ = 'instance'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Unicode, unique=True, nullable=False)
    name = db.Column(db.Unicode())
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

def fetch_and_print_instances():
    route = "https://galaxyproject.org/assets/data/use/index.json"
    payload_reference = "data.platforms.edges[].node.platforms[]"
    try:
        response = requests.get(route, timeout=10)
        response.raise_for_status()
        data = response.json()
        platforms = jmespath.search(payload_reference, data)
        for platform in platforms:
            print(f"{platform.get('name', '')}: {platform.get('platform_url', '')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fetch_and_print_instances()
