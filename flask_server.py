from flask import Flask, jsonify, request
import sys, os, re, csv, codecs, numpy as np, pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import *
from keras.models import Model
from keras import initializers, regularizers, constraints, optimizers, layers
import pickle

app = Flask(__name__)
max_words = 30000
max_len = 100

def BiLSTM():
    X_inp = Input( shape=(max_len,) )
    X = Embedding(max_words, 128)(X_inp)
    X = Bidirectional(LSTM(200, return_sequences=True))(X)
    X = Dropout(0.1)(X)
    X = LSTM(100, return_sequences=True)(X)
    X = GlobalAvgPool1D()(X)
    X = Dense(50, activation='relu')(X)
    X = Dropout(0.1)(X)
    X = Dense(6, activation='sigmoid')(X)
    model  = Model(inputs=X_inp, outputs=X)
    model.load_weights('toxicity_model2_weights.h5')
    return model

def predict(sentence):
    model = BiLSTM()
    with open('tokenizer.pk', 'rb') as tk:
        tokenizer = pickle.load(tk)
    sentence = sentence.lower()
    inp_tokenized = tokenizer.texts_to_sequences([sentence])
    final_inp = pad_sequences(inp_tokenized, maxlen=max_len, padding='post')
    return model.predict(final_inp)



@app.route("/test", methods=['GET'])
def test():
    comment = request.args.get('comment')
    prediction = predict(comment)
    resp = ""
    for val in prediction[0]:
        resp = resp + str(format(val*100, '.2f')) + ","
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
