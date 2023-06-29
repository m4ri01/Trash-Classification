import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, render_template, request, redirect, url_for, flash
from keras.models import load_model
import cv2
import numpy as np
import json

app = Flask(__name__,template_folder='template')
model = load_model('model_sampah_mobilenet.h5')
label = {0:"Anorganik",1:"B3",2:"Organik"}

def model_predict():
    img = cv2.imread('static/uploaded_file.jpg')
    resized = cv2.resize(img,(224,224))
    normalized = resized/255.0
    reshaped=np.reshape(normalized,(1,224,224,3))
    reshaped=np.vstack([reshaped])
    result = model.predict(reshaped)
    get_keys=np.argmax(result,axis=1)[0]
    result = {"result":label[get_keys]}
    return result


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']
        file.save('static/uploaded_file.jpg')
        result = model_predict()
        return json.dumps(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)