import pickle 
import pandas as pd

class SentimentAnalysis:
    def __init__(self):
        with open('model.pickle', 'rb') as handle:
            self.words_counter = pickle.loads(handle.read())

        self.train_reviews_df = pd.read_csv("./src/data/train.csv")
        self.train_reviews_df = self.train_reviews_df[:25000]
        self.train_reviews_df["review"] = self.train_reviews_df["review"].apply(self.clean_review)

        self.p_pos = len(self.train_reviews_df[self.train_reviews_df["sentiment"] == 'positive']) / len(self.train_reviews_df)
        self.p_neg = len(self.train_reviews_df[self.train_reviews_df["sentiment"] == 'negative']) / len(self.train_reviews_df)
        self.all_words = list(self.words_counter.keys())

        self.total_pos = len(self.train_reviews_df[self.train_reviews_df["sentiment"] == "positive"])
        self.total_neg = len(self.train_reviews_df[self.train_reviews_df["sentiment"] == "negative"])

    def clean_review(self, review: str) -> str:
            review = review.lower()
            review = review.replace("<br>", "").replace("<br />", "")

            res = ""

            for char in review:
                if (char.isalpha() or char == " "): 
                    res += char

            return res

    def analize(self, phrase: str) -> str:
        p_res_pos = 1
        p_res_neg = 1
        has = {}

        for word in self.all_words:
            if (word in phrase):
                has[word] = True
            else:
                has[word] = False

        for word in has:
            if (has[word]):
                p_word_given_positive = (self.words_counter[word]["positive"] / self.total_pos)
                p_word_given_negative = (self.words_counter[word]["negative"] / self.total_neg)

                p_word = self.words_counter[word]["total"] / len(self.train_reviews_df)

                p_positive_given_word = p_word_given_positive / p_word
                p_negative_given_word = p_word_given_negative / p_word
                
                if (p_negative_given_word > 0):
                    p_res_neg *= p_negative_given_word

                if (p_positive_given_word > 0):
                    p_res_pos *= p_positive_given_word
            else:
                p_n_word_given_positive = 1 - (self.words_counter[word]["positive"] / self.total_pos)
                p_n_word_given_negative = 1 - (self.words_counter[word]["negative"] / self.total_neg)

                p_n_word = 1 - (self.words_counter[word]["total"] / len(self.train_reviews_df))

                p_positive_given_n_word = p_n_word_given_positive / p_n_word
                p_negative_given_n_word = p_n_word_given_negative / p_n_word
                
                if (p_negative_given_n_word > 0):
                    p_res_neg *= p_negative_given_n_word
                
                if (p_positive_given_n_word > 0):
                    p_res_pos *= p_positive_given_n_word
        
        p_res_neg *= self.p_neg
        p_res_pos *= self.p_pos

        result = "positive"

        if (p_res_pos < p_res_neg):
            result = "negative"

        return result
        