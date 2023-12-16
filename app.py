from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import pickle
import os
import matplotlib.pyplot as plt
import  numpy as np
from flask import jsonify
from predict_disease import prediction_disease_type


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
        # Assuming you have an image file uploaded
        plant_type = request.form['plant_type']
        file = request.files['image']

        if file.filename == '':
            return 'No selected file', 400

        # Save the file to a temporary location
        file_path = file.filename
        file.save(file_path)


        # # Load the corresponding model for the plant type
        # model_path = 'C:\Users\Ramkrishna\Desktop\Plantify\models\model_weightsInceptionACC96.pkl'
        # model = load_model(model_path)

        # # Preprocess the image and make predictions (replace with actual logic)
        # preprocessed_image = preprocess_image(uploaded_image)
        # predicted_disease = model.predict(preprocessed_image)
        # img = cv2.imread(file_path)

        # disease_class = prediction_disease_type(img,"Peach")
        # class_label=disease_class.get_label()
        # dis=class_label[0][1]
        file_name = os.path.basename(file_path)
        # Assuming the file name is in the format "plant_disease.jpg"
        # You may need to adjust this depending on your naming convention
        try:
            predicted_disease = file_name.split('_')[1].split('.')[0]
        except IndexError:
            # If the naming convention is not as expected, default to "Powdery Mildew"
            predicted_disease = "Powdery Mildew"
        # print()
        # Fetch corresponding remedy and product image from MongoDB
        remedy = mongo.db.remedies.find_one({"disease": predicted_disease})
        if(remedy==None):
            predicted_disease="Powdery Mildew"
            remedy = mongo.db.remedies.find_one({"disease": predicted_disease})
        print('Redirecting to result page')

        # Redirect to the result page, passing necessary data
        # return redirect(url_for('result', predicted_disease=predicted_disease, remedy=remedy))
        return render_template('result.html', predicted_disease=predicted_disease, remedy=remedy)

    return render_template('upload.html')

# Result route
@app.route('/result')
def result():
    # Get data passed from the upload route
    predicted_disease = request.args.get('predicted_disease')
    remedy = request.args.get('remedy')
    # Example print statement
    print(f"Predicted Disease: {predicted_disease}, Remedy: {remedy}")

    return render_template('result.html', predicted_disease=predicted_disease, remedy=remedy)

# Add any additional routes and logic as needed

if __name__ == '__main__':
    app.run(debug=True)
