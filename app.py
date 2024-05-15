from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import prediction using trained NN
from predict import predict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nnimages.db'

db = SQLAlchemy(app)

class Image(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	filename = db.Column(db.String(100))
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Image %r>' % self.id

with app.app_context():
	db.create_all()

@app.route('/', methods = ['POST', 'GET'])
def index():
	return render_template('index.html')

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
	if request.method == "POST":
		if 'image' not in request.files:
			return "No image uploaded", 400
		image_file = request.files['image']
		if image_file:
			# Save the image file to a folder on your server
			image_path = f"static/images/{image_file.filename}"
			image_file.save(image_path)
	        
	        # Store the image path in the database
			new_image = Image(filename=image_path)
			db.session.add(new_image)
			db.session.commit()
            
            # Run model on uploaded image
			prediction = predict(image_path)
			print(prediction)
	        
			return render_template('uploaded.html', image = new_image)
		else:
			return "Invalid file format", 400
	else:
		return "You probably won't see this."

if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()