from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import login_required, UserMixin

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cb.sqlite'
app.config['SECRET_KEY'] = '61da80092ef554ebb1c8144e5c0059aa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	password = db.Column(db.String(80))
	

class List(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	item = db.Column(db.String(150))

@app.route('/')

def home():

	todo_list = List.query.all()
	return render_template('home.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():

	item = request.form.get('item')
	save_item = List(item=item)
	db.session.add(save_item)
	db.session.commit()
    
	return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = List.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/register', methods=['GET', 'POST'])
def register():

	form = RegisterForm()

	if request.method == 'POST':
		hsh = generate_password_hash(form.password.data, method="sha256")
		new_user = User(username=form.username.data, password=hsh)
		db.session.add(new_user)
		db.session.commit()
		flash('you are a now a user now login in')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

	form = LoginForm()

	if request.method =='POST':
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				
				return redirect(url_for('home'))

		
	return render_template('login.html', form=form)

2



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
