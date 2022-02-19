from flask import Flask, url_for, request, flash, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'


class SubmitForm(FlaskForm):
	f_name = StringField("First Name", validators=[DataRequired(), Length(20)])
	l_name = StringField("Last Name", validators=[DataRequired(), Length(20)])
	email = StringField("Email", validators=[DataRequired(), Length(20)])
	phone_number = StringField("Phone Number", validators=[DataRequired(), Length(20)])
	remember_me = BooleanField("remember me")
	
@app.route('/home')
def home():
	form = SubmitForm()
	
	return render_template('home.html', form=form)


if __name__ =="__main__":
	app.run(debug=True)