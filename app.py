from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "aed6c9be02818d13f2f60a61f33cf1fa0e40edd7a6db6ac9eca7962debc84a41"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # type: ignore

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
                password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(username=username, password=password_hash) # type: ignore
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login")) 
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                password_correct = bcrypt.check_password_hash(user.password, password) 
                if password_correct:
                    login_user(user)
                    return redirect(url_for('dashboard'))
                else:
                    return render_template("login_details_incorrect.html")
        else:
            return render_template("login_details_incorrect.html")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)