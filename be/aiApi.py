import base64
from io import BytesIO
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array
from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)
CORS(app, supports_credentials=False, methods=["GET", "POST", "PUT", "DELETE"])

# Load pre-trained model
loaded_model = tf.keras.models.load_model('D:\\Workspace\\Tren truong\\iot\\be\\Iot (1).h5')

@app.route("/ai", methods=["POST"])
def ai():
    try:
        data = request.get_json()
        image_data = data.get('image')

        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400

        # Decode base64 image data
        image_binary = base64.b64decode(image_data.split(',')[1])  # Extract base64-encoded part

        # Open the image using PIL
        image = Image.open(BytesIO(image_binary))

        # Save the image to a file
        output_path = 'D:\\Workspace\\Tren truong\\iot\\be\\ai.jpg'  # Specify the desired file path
        image.save(output_path, 'JPEG')

        # Load the saved image for prediction
        img = load_img(output_path, target_size=(128, 128))
        img = img_to_array(img)
        img = img / 255.0

        # Reshape the image to match the model's expected shape
        img = np.expand_dims(img, axis=0)

        # Make predictions
        predictions = loaded_model.predict(img)
        predicted_class_index = np.argmax(predictions)
        confidence = np.max(predictions) * 100

        label_to_class = {0: 'CayCaChua', 1: 'CayChuoi', 2: 'CaiThao', 3: 'CayLua', 4: 'DuaChuot', 5: 'SupLo'}
        predicted_class = label_to_class[predicted_class_index]
        
        result = {
            'predicted_class': predicted_class,
            'confidence': confidence
        }

        print(predicted_class_index)
        return jsonify(result)

    except Exception as e:
        error_message = f"Error during prediction: {str(e)}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
