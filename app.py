#!/usr/bin/env python
# coding: utf-8


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
from flask_cors import CORS

from keras.models import model_from_json
from keras.optimizers import RMSprop
from keras.preprocessing import sequence

app = Flask(__name__)
CORS(app)
api = Api(app)

#load tokenizer
vec_path = 'models/Tokenizer.pkl'
with open(vec_path, 'rb') as f:
  tokenizer = pickle.load(f)

# load json and create model
json_file = open('models/UitClassifier.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# load weights
model.load_weights("models/model.h5")

model.compile(loss='binary_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')


class PredictSentiment(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']

        # vectorize the user's query and make a prediction
        X_test = np.array([user_query])
        test_sequences = tokenizer.texts_to_sequences(X_test)
        test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=150)
        
        # make prediction
        prediction = model.predict(test_sequences_matrix)
        confidence = prediction[0]

        # Output either 'Male' or 'Female' and calculate confidence rate
        if confidence[0] < 0.5:
            pred_text = 'Female'
            confidence = round((1-confidence[0])*100,2)
        else:
            pred_text = 'Male'
            confidence = round(confidence[0]*100,2)

        # create JSON object
        output = {'prediction': pred_text, 'confidence': confidence}
        
        return output


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictSentiment, '/api/predict')

@app.route('/')
def index():
    return "<h1>Welcome to our webapi!</h1>"

if __name__ == '__main__':
    app.run(debug=True)

