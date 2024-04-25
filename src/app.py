from flask import Flask, request, jsonify
import json
import datetime
import pickle
import pandas as pd
import math
from model.SentimentAnalysis import SentimentAnalysis

app = Flask(__name__)

sentiment_analysis = SentimentAnalysis()

@app.route("/sentiment", methods=["GET"])
def init():
    if ("phrase" not in request.headers): 
        return {"status": "error", "message": "Missing phrase"}, 400
    elif (request.headers["phrase"] == "" or not request.headers["phrase"]):
        return {"status": "error", "message": "Please send a valid phrase"}, 400

    result = sentiment_analysis.analize(request.headers["phrase"])

    return {"result": result}, 200



if __name__ == '__main__':
    app.run(debug=True, port=5500, host="0.0.0.0")