from flask import Flask, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
app.secret_key = "rob"
bootstrap = Bootstrap5(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


@app.route("/")
def home():
    all_cafes = Cafe.query.order_by(Cafe.id).all()
    cafe_list = [all_cafes]
    return render_template('index.html', cafes=cafe_list)

@app.route("/add")
def add_cafe():
    pass


@app.route("/delete")
def delete_cafe():
    pass


@app.route("/<int:id>")
def show_cafe(id):
    req_cafe = db.get_or_404(Cafe, id)
    return render_template('cafe.html', cafe=req_cafe)


if __name__ == '__main__':
    app.run(debug=True)