from flask import Flask, render_template, request, redirect, url_for, Markup
from flask_pymongo import PyMongo
import pickle
import os
from model import predict_image

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/plantify"
app.static_folder = "static/"
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
        plant_type = request.form['plant_type']
        file = request.files['image']

        # if file.filename == '':
        #     return 'No selected file', 400

        # # Save the file to a temporary location
        # file_path = os.path.join('static/uploads', file.filename)
        # file.save(file_path)

        # Read image data and predict disease
        img = file.read()
        try:
            prediction = predict_image(img)
            predicted_disease = prediction
        except Exception as e:
            print(f"Prediction error: {e}")
            return 'Error in prediction', 500

        # Fetch corresponding remedy from MongoDB
        remedy = mongo.db.remedies.find_one({"disease": predicted_disease})
        if remedy is None:
            predicted_disease = "Powdery Mildew"
            remedy = mongo.db.remedies.find_one({"disease": predicted_disease})

        # Redirect to the result page, passing necessary data
        return render_template('result.html', predicted_disease=predicted_disease, remedy=remedy)

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
