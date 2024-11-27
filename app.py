from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = "dog_cat.h5"
model = load_model(MODEL_PATH)

# Define class labels
CLASS_NAMES = {0: "Cat", 1: "Dog"}

# API Endpoint to process image uploads
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # Preprocess the image
    try:
        image = Image.open(file).convert("RGB")
        image = image.resize((256, 256))  # Resize to model input size
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0) / 255.0

        # Make prediction
        prediction = model.predict(image_array)
        label = int(prediction[0] > 0.5)  # 0 = Cat, 1 = Dog
        return jsonify({"label": CLASS_NAMES[label]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve the frontend
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
