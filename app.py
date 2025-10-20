from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():          
    if request.method == "POST":
        # Getting the user details and adding them to the database
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return render_template("username_already_taken.html")
            else:    
                password_hash = bcrypt.generate_password_hash('password')
                new_user = User(username=username, password=password_hash)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login")) 
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)