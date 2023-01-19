from flask import (Flask, render_template, request, redirect, url_for)
from model import connect_to_db, db

app = Flask(__name__)
app.secret_key = "dev"

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)