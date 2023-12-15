from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import pickle

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017"
mongo = PyMongo(app)

# Function to load pickled models
def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Assuming you have an image file uploaded
        uploaded_image = request.files['image']
        plant_type = request.form['plant_type']

        # Load the corresponding model for the plant type
        model_path = f'models/{plant_type}_model.pkl'
        model = load_model(model_path)

        # Preprocess the image and make predictions (replace with actual logic)
        preprocessed_image = preprocess_image(uploaded_image)
        predicted_disease = model.predict(preprocessed_image)

        # Fetch corresponding remedy and product image from MongoDB
        remedy = mongo.db.remedies.find_one({"disease": predicted_disease})

        # Redirect to the result page, passing necessary data
        return redirect(url_for('result', predicted_disease=predicted_disease, remedy=remedy))

    return render_template('upload.html')

# Result route
@app.route('/result')
def result():
    # Get data passed from the upload route
    predicted_disease = request.args.get('predicted_disease')
    remedy = request.args.get('remedy')

    return render_template('result.html', predicted_disease=predicted_disease, remedy=remedy)

# Add any additional routes and logic as needed

if __name__ == '__main__':
    app.run(debug=True)
