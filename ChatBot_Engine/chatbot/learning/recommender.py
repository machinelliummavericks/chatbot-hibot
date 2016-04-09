#from fastFM.mcmc import FMClassification, FMRegression
from fastFM.als import FMClassification, FMRegression
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import OneHotEncoder
pd.options.mode.chained_assignment = None
from sklearn.externals import joblib

class Recommender:
    """
    Recommender class to predict movie ratings for a user.

    Recommendation engine is built on Factorization Machines and uses
    the following code base: https://github.com/ibayer/fastFM

    @Usage:
        learn = Recommender()
        X,y = learn.load_training_users()
        X_encoded = learn.encode_train_data(X)
        learn.fit(X_encoded, y)
        learn.save_model()
    """

    def __init__(self):

        self.base = os.path.dirname(os.path.realpath(__file__)) + '/'

        self.training_users = 0
        self.clf = 0
        self.encoder = 0

        self.b_age = 0
        self.labels = ['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79','80-89','90-99']
        self.b_gender = 0


    def load_training_users(self):
        """
        Load Fake user data and format features
        """
        u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
        users = pd.read_csv(self.base+'ml-100k/u.user', sep='|', names=u_cols,
                            encoding='latin-1')

        r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
        ratings = pd.read_csv(self.base+'ml-100k/u.data', sep='\t', names=r_cols,
                              encoding='latin-1')

        m_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url',
                  'unknown','Action','Adventure','Animation','Children','Comedy','Crime',
                  'Documentary','Drama','Fantasy','FilmNoir','Horror','Musical','Mystery',
                  'Romance','SciFi','Thriller','War','Western']
        movies = pd.read_csv(self.base+'ml-100k/u.item', sep='|', names=m_cols,
                             encoding='latin-1')

        # create one merged DataFrame
        movie_ratings = pd.merge(movies, ratings)
        lens = pd.merge(movie_ratings, users)

        _cols = ['user_id','movie_id','age','sex',
                 #'occupation','zip_code','release_date',
                 'unknown','Action','Adventure','Animation','Children','Comedy','Crime',
                 'Documentary','Drama','Fantasy','FilmNoir','Horror','Musical','Mystery',
                 'Romance','SciFi','Thriller','War','Western']

        X = lens[_cols]
        y = lens['rating']

        ## AGE
        age_group = pd.cut(X.age, range(0, 101, 10), right=False, labels=self.labels)
        self.b_age=pd.get_dummies(age_group)
        X['age'] = self.b_age.values.argmax(1)

        ## GENDER
        self.b_gender=pd.get_dummies(X['sex'])
        X['sex'] = self.b_gender.values.argmax(1)

        '''
        ## Job
        b=pd.get_dummies(X['occupation'])
        X['occupation'] = b.values.argmax(1)

        ## zip_code
        b=pd.get_dummies(X['zip_code'])
        X['zip_code'] = b.values.argmax(1)

        ## release_date
        b=pd.get_dummies(X['release_date'])
        X['release_date'] = b.values.argmax(1)
        '''
        return X,y


    def get_age(self, df):
        """
        Turn user age into dummy variable
        """
        age_group = pd.cut(df.age, range(0, 101, 10), right=False, labels=self.labels)
        age_group = pd.get_dummies(age_group)
        age_group = age_group.reindex(columns = self.b_age.columns, fill_value=0)
        return age_group.values.argmax(1)

    def get_gender(self, df):
        """
        Turn user gender into dummy variable
        """
        gender_group = pd.get_dummies(df.sex)
        gender_group = gender_group.reindex(columns = self.b_gender.columns, fill_value=0)
        return gender_group.values.argmax(1)

    def encode_train_data(self, X):
        """
        One-Hot encode training data
        """
        self.encoder = OneHotEncoder(handle_unknown='ignore', categorical_features='all').fit(X)
        X = self.encoder.transform(X)
        return X

    def transform_new_data(self, X):
        """
        Transform new user data by One-Hot encoding
        """
        return self.encoder.transform(X)

    def fit(self, X, y):
        """
        Fit model
        """
        rank=8
        n_iter=100
        self.clf = FMRegression(rank=rank, n_iter=n_iter)
        self.clf.fit(X, y)

    def save_model(self):
        """
        Save model
        """
        joblib.dump(self.clf, self.base+'fastML_models/fastFM.pkl')

    def load_model(self):
        """
        Load model
        """
        self.clf = joblib.load(self.base+'fastML_models/fastFM.pkl')

    def predict(self, X):
        """
        Predict ratings
        """
        return self.clf.predict(X)



if __name__ == '__main__':

        learn = Recommender()
        X,y = learn.load_training_users()
        X_encoded = learn.encode_train_data(X)
        learn.fit(X_encoded, y)
        learn.save_model()

