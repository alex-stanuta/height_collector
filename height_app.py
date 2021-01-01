from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from send_email import send_email

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hlxqdxijupuvgv:022a9fa7a8751930a3a186cef444048066fa3cb7686c080892fce0ea2b8af74f@ec2-52-200-16-99.compute-1.amazonaws.com:5432/d54ij65iqt2p25?sslmode=require'
db = SQLAlchemy(app)

class Data(db.Model):
	__tablename__ = 'data'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	height = db.Column(db.Integer)

	def __init__(self, email, height):
		self.email = email
		self.height = height


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
	if request.method == 'POST':
		email = request.form["email"]
		height = request.form["height"]
		if db.session.query(Data).filter(Data.email == email).count() == 0:
			data = Data(email, height)
			db.session.add(data)
			db.session.commit()
			no_users = round(db.session.query(func.count(Data.height)).scalar())
			average_height = round(db.session.query(func.avg(Data.height)).scalar(), 1)
			send_email(email, height, average_height, no_users)
			return render_template("success.html")
		return render_template("failure.html")

if __name__ == "__main__":
	app.debug = True
	app.run()