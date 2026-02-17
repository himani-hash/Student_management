from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import api
from models import db


load_dotenv()

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///student.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)
