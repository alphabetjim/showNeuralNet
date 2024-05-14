from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nnimages.db'
db = SQLAlchemy(app)

class Image(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	filename = db.Column(db.String(100))
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Image %r>' % self.id

# with app.app_context():
# 	db.create_all()

@app.route('/', methods = ['POST', 'GET'])
def index():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)