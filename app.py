from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import prediction using trained NN
from predict import predict
import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = "ddfqaz73q", 
    api_key = "431974138645946", 
    api_secret = "xs3XhQ2TUNCSrMg5-EUkYLveU-0", # Click 'View Credentials' below to copy your API secret
    secure=True
)

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
    public_ids = ["dogsorcats/dogorcat"]
    image_delete_result = cloudinary.api.delete_resources(public_ids, resource_type="image", type="upload")
    print(image_delete_result)
    return render_template('index.html')

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
	if request.method == "POST":
		if 'image' not in request.files:
			return "No image uploaded", 400
		image_file = request.files['image']
		if image_file:
			# Save the image file to a folder on your server
			#image_path = f"static/images/{image_file.filename}"
			#image_file.save(image_path)
            # Save image to cloudinary
			upload_result = cloudinary.uploader.upload(image_file, public_id="dogorcat", folder="dogsorcats")
			print(upload_result)
			print(upload_result["secure_url"])
            
            # Optimize delivery by resizing and applying auto-format and auto-quality
			optimize_url, _ = cloudinary_url("dogsorcats/dogorcat", fetch_format="auto", quality="auto")
			print(optimize_url)
	        
	        # delete any existing Image entries
			img_query = Image.query
			total_imgs = img_query.count()
			print(f"Total images in db: {total_imgs}")
			if total_imgs > 0:
				db.session.query(Image).delete()
				db.session.commit()
            
            # Store the image path in the database
			new_image = Image(filename=optimize_url)
			db.session.add(new_image)
			db.session.commit()
            
            # Run model on uploaded image
			prediction = predict(upload_result["secure_url"])#optimize_url)
			print(prediction)
	        
			return render_template('uploaded.html', image = upload_result["secure_url"], prediction = prediction)
		else:
			return "Invalid file format", 400
	else:
		return "You probably won't see this."

if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()