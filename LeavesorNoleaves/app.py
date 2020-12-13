# Flask libraries
from flask import Flask, request, jsonify, make_response
#lib for base64 conversion
import base64
# lib for interacting with the operating system
import os
#API Jason files
from flask_restful import Resource, Api
import json
# import random
#tensorflow libraries
from tensorflow import keras
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

#loading preprocessed model
model = load_model("/home/swapnil/Desktop/inception_v3_299x299.model")

#predicting given image is leaf or not
def predict_binary(image_name):
    img = image.load_img(image_name, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    if preds[0][0] < 0.55:
        return ("Leaves")
    else:
        return ("No Leaves")

application= app = Flask(__name__)
api=Api(application)


class GetPrediction(Resource):
    def get(self):
        return make_response(jsonify({"about": "hello world"}), 200)
    def post(self):
        json_data=request.get_json(force=True)
        img_list  = json_data['image_list'] 
        predict_list=[]
        if len(img_list)!=0:
            for imgstring in img_list: 
                if len(imgstring) !=0:
                    # Converting base64 into byte
                    imgdata = base64.b64decode(imgstring) 
                    filename = 'predict_image.jpg' 
                    with open(filename, 'wb') as f: 
                        # Creating Image out of byte
                        f.write(imgdata) 
                    # call the function to detect leaf or not
                    class_binary = predict_binary(filename)
                    predict_list.append(class_binary)                 
                else:
                    predict_list.append("Image length is 0")
            return make_response(jsonify({
                        "predict":predict_list
                    }),200)    
        else:
            return make_response(jsonify({"Error": "Please select the Image"}), 400)
        # checking whether request body contains data
        # If not contained data sending error stating 'Select the Image'
            

api.add_resource(GetPrediction, '/')
if __name__ == '__main__':
  # running application on host 'localhost' and port '5000'
  application.run(host='0.0.0.0', debug=True) 