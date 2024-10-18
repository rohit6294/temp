from flask import Flask, render_template, request, jsonify
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load the model
model = load_model(r'C:\Users\rohit\Desktop\images_classify\Image_classifier.keras')
data_cat = ['battery', 'cardboard', 'food_waste', 'glass', 'metal', 'paper', 'plastic']

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

img_height = 180
img_width = 180

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'result': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'result': 'No selected file'})

    # Save the uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Load and preprocess the image
    image_load = tf.keras.utils.load_img(filepath, target_size=(img_height, img_width))
    img_arr = tf.keras.utils.img_to_array(image_load)  # Use img_to_array instead of array_to_img
    img_bat = np.expand_dims(img_arr, axis=0)  # Add batch dimension

    # Perform prediction
    predict = model.predict(img_bat)
    score = tf.nn.softmax(predict)

    # Get the prediction result
    predicted_class = data_cat[np.argmax(score)]
    accuracy = np.max(score) * 100

    result = f'Image is {predicted_class} with accuracy of {accuracy:.2f}%'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
