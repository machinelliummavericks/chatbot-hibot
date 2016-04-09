import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
pd.options.mode.chained_assignment = None
from sklearn.externals import joblib
from sklearn.cluster import KMeans
import os

class Segmentation:
    """
    Segmentation class to predict cluster that user belong to.

    Segmentation engine is built k-means clustering

    @TODO: Look into k-modes clustering to deal with categorical data

    @Usage:
        cluster = Segmentation()
        X = learn.load_training_users()
        X_encoded = cluster.encode_train_data(X)
        cluster.fit(X_encoded)
        cluster.save_model()
    """

    def __init__(self):

        self.base = os.path.dirname(os.path.realpath(__file__)) + '/'

        self.training_users = 0
        self.clf = 0
        self.encoder = 0
        self.cluster_labels = 0

        self.features = ['user_id', 'movie_id', 'Age_0-9', 'Age_10-19', 'Age_20-29', 'Age_30-39',
                         'Age_40-49', 'Age_50-59', 'Age_60-69', 'Age_70-79', 'Age_80-89', 'Age_90-99',
                         'Gender_F', 'Gender_M']

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

        _cols = ['user_id','movie_id','rating','age','sex']

        X = lens[_cols]

        ## AGE
        age_group = pd.cut(X.age, range(0, 101, 10), right=False, labels=self.labels)
        self.b_age=pd.get_dummies(age_group, prefix='Age')

        ## GENDER
        self.b_gender=pd.get_dummies(X['sex'], prefix='Gender')

        ## Merge all back
        X = pd.concat((X,self.b_age,self.b_gender), axis=1)

        ## Keep only these features
        X = X[self.features]

        return X

    def get_age(self, df):
        """
        Turn user age into dummy variable
        """
        age_group = pd.cut(df.age, range(0, 101, 10), right=False, labels=self.labels)
        age_group = pd.get_dummies(age_group, prefix='Age')
        age_group = age_group.reindex(columns = self.b_age.columns, fill_value=0)
        return age_group.values[0]

    def get_gender(self, df):
        """
        Turn user gender into dummy variable
        """
        gender_group = pd.get_dummies(df.sex, prefix='Gender')
        gender_group = gender_group.reindex(columns = self.b_gender.columns, fill_value=0)
        return gender_group.values[0]

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

    def fit(self, X):
        """
        Fit model
        """
        self.clf = KMeans(n_clusters=10)
        self.clf.fit(X)
        #self.cluster_labels = self.clf.labels

    def save_model(self):
        """
        Save model
        """
        joblib.dump(self.clf,self.base+'segmentation_models/clusters.pkl')

    def load_model(self):
        """
        Load model
        """
        self.clf = joblib.load(self.base+'segmentation_models/clusters.pkl')

    def predict(self, X):
        """
        Predict user cluster
        """
        return self.clf.predict(X)



if __name__ == '__main__':

        cluster = Segmentation()
        X = cluster.load_training_users()
        X_encoded = cluster.encode_train_data(X)
        cluster.fit(X_encoded)
        cluster.save_model()

