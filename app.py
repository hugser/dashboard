from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap  
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user
from flask_login.mixins import UserMixin



from wtforms import StringField, PasswordField
from wtforms.validators import Length, Email

from werkzeug.security import generate_password_hash, check_password_hash

from dash_application import create_dash_application



app = Flask(__name__)
app.config["SECRET_KEY"] = "THIS IS A SECRET"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager()
login.init_app(app)
create_dash_application(app)


@login.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)


class loginForm(FlaskForm):
    email = StringField("email",validators=[Email()])
    password = PasswordField("password", validators=[Length(min=5)])

class registerForm(FlaskForm):
    email = StringField("email",validators=[Email()])
    password = PasswordField("password", validators=[Length(min=5)])
    repeat_password = PasswordField("repeat_password", validators=[Length(min=5)])



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET","POST"])
def login():
    form = loginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if check_password_hash(user.password,form.password.data):
            login_user(user)

            return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route("/register",  methods=["GET","POST"])
def register():
    form = registerForm()

    if form.validate_on_submit() and form.password.data == form.repeat_password.data:
        user = User(
            email = form.email.data,
            password = generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
    
        return redirect(url_for("index"))

    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


#@app.route("/potato")
#@login_required
#def potato():
#    return "Potato"

if __name__=="__main__":
    app.run()