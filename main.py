from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
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


class CreateCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Google Maps Location Link", validators=[DataRequired(), URL()])
    img_url = StringField("Cafe Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location Name", validators=[DataRequired()])
    seats = StringField("Number Of Seats", validators=[DataRequired()])
    has_toilet = SelectField("Are there restrooms available?",choices=[(0, 'No'),(1,"Yes")], validators=[DataRequired()])
    has_wifi = SelectField("Does this Cafe offer Wifi?",choices=[(0, 'No'),(1,"Yes")], validators=[DataRequired()])
    has_sockets = SelectField("Are there power outlets available?",choices=[(0, 'No'),(1,"Yes")], validators=[DataRequired()])
    can_take_calls = SelectField("Can you take phone calls?",choices=[(0, 'No'),(1,"Yes")], validators=[DataRequired()])
    coffee_price = StringField("Estimated price of coffee.",choices=[(0, 'No'),(1,"Yes")], validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route("/")
def home():
    all_cafes = Cafe.query.order_by(Cafe.id).all()
    cafe_list = [all_cafes]
    return render_template('index.html', cafes=cafe_list)

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CreateCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.location.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)

@app.route("/<int:id>")
def show_cafe(id):
    req_cafe = db.get_or_404(Cafe, id)
    return render_template('cafe.html', cafe=req_cafe)


if __name__ == '__main__':
    app.run(debug=True)