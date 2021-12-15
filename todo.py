from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cb.sqlite'
app.config['SECRET_KEY'] = '61da80092ef554ebb1c8144e5c0059aa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
