from flask import Flask, request, jsonify
import json
import datetime
import pickle
import pandas as pd
import math

app = Flask(__name__)

def clean_review(review: str):
    review = review.lower()
    review = review.replace("<br>", "").replace("<br />", "")

    res = ""

    for char in review:
        if (char.isalpha() or char == " "): 
            res += char

    return res

with open('model.pickle', 'rb') as handle:
    words_counter = pickle.loads(handle.read())

train_reviews_df = pd.read_csv("data/train.csv")
train_reviews_df = train_reviews_df[:25000]
train_reviews_df["review"] = train_reviews_df["review"].apply(clean_review)

p_pos = len(train_reviews_df[train_reviews_df["sentiment"] == 'positive']) / len(train_reviews_df)
p_neg = len(train_reviews_df[train_reviews_df["sentiment"] == 'negative']) / len(train_reviews_df)
all_words = list(words_counter.keys())

total_pos = len(train_reviews_df[train_reviews_df["sentiment"] == "positive"])
total_neg = len(train_reviews_df[train_reviews_df["sentiment"] == "negative"])

@app.route("/sentiment", methods=["GET"])
def init():
    if ("phrase" not in request.headers): 
        return {"status": "error", "message": "Missing phrase"}, 400
    elif (request.headers["phrase"] == "" or not request.headers["phrase"]):
        return {"status": "error", "message": "Please send a valid phrase"}, 400

    phrase = request.headers["phrase"]

    p_res_pos = 1
    p_res_neg = 1
    has = {}

    for word in all_words:
        if (word in phrase):
            has[word] = True
        else:
            has[word] = False

    for word in has:
        if (has[word]):
            p_word_given_positive = (words_counter[word]["positive"] / total_pos)
            p_word_given_negative = (words_counter[word]["negative"] / total_neg)

            p_word = words_counter[word]["total"] / len(train_reviews_df)

            p_positive_given_word = p_word_given_positive / p_word
            p_negative_given_word = p_word_given_negative / p_word
            
            if (p_negative_given_word > 0):
                p_res_neg *= p_negative_given_word

            if (p_positive_given_word > 0):
                p_res_pos *= p_positive_given_word
        else:
            p_n_word_given_positive = 1 - (words_counter[word]["positive"] / total_pos)
            p_n_word_given_negative = 1 - (words_counter[word]["negative"] / total_neg)

            p_n_word = 1 - (words_counter[word]["total"] / len(train_reviews_df))

            p_positive_given_n_word = p_n_word_given_positive / p_n_word
            p_negative_given_n_word = p_n_word_given_negative / p_n_word
            
            if (p_negative_given_n_word > 0):
                p_res_neg *= p_negative_given_n_word
            
            if (p_positive_given_n_word > 0):
                p_res_pos *= p_positive_given_n_word
    
    p_res_neg *= p_neg
    p_res_pos *= p_pos

    result = "positive"

    if (p_res_pos < p_res_neg):
        result = "negative"

    return {"result": result}, 200



if __name__ == '__main__':
    app.run(debug=True, port=5500, host="0.0.0.0")