import numpy as np
import pandas as pd
import cPickle as pickle
from sklearn.metrics import roc_auc_score, mean_squared_error, accuracy_score

#from fastFM.mcmc import FMClassification, FMRegression
from fastFM.als import FMClassification, FMRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.datasets import dump_svmlight_file

pd.options.mode.chained_assignment = None

# pass in column names for each CSV
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('ml-100k/u.user', sep='|', names=u_cols,
                    encoding='latin-1')

r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=r_cols,
                      encoding='latin-1')

# the movies file contains columns indicating the movie's genres
# let's only load the first five columns of the file with usecols
m_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url',
          'unknown','Action','Adventure','Animation','Children','Comedy','Crime',
          'Documentary','Drama','Fantasy','FilmNoir','Horror','Musical','Mystery',
          'Romance','SciFi','Thriller','War','Western']
#m_cols = ['movie_id', 'title', 'release_date', 'video_release_date']
movies = pd.read_csv('ml-100k/u.item', sep='|', names=m_cols, #usecols=range(5),
                     encoding='latin-1')

# create one merged DataFrame
movie_ratings = pd.merge(movies, ratings)
lens = pd.merge(movie_ratings, users)

_cols = ['user_id','movie_id','age','sex','occupation','zip_code','release_date',
         'unknown','Action','Adventure','Animation','Children','Comedy','Crime',
         'Documentary','Drama','Fantasy','FilmNoir','Horror','Musical','Mystery',
         'Romance','SciFi','Thriller','War','Western']

X = lens[_cols]
y = lens['rating']

## AGE
labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99']
age_group = pd.cut(X.age, range(0, 101, 10), right=False, labels=labels)
b=pd.get_dummies(age_group)
X['age'] = b.values.argmax(1)

## GENDER
b=pd.get_dummies(X['sex'])
X['sex'] = b.values.argmax(1)

## Job
b=pd.get_dummies(X['occupation'])
X['occupation'] = b.values.argmax(1)

## zip_code
b=pd.get_dummies(X['zip_code'])
X['zip_code'] = b.values.argmax(1)

## release_date
b=pd.get_dummies(X['release_date'])
X['release_date'] = b.values.argmax(1)

print lens.columns
print X.head()
print y.head()

trainX = X[0:80000]
testX  = X[80000:100000]
trainY = y[0:80000]
testY  = y[80000:100000]

encoder = OneHotEncoder(handle_unknown='ignore', categorical_features='all').fit(trainX)
trainX = encoder.transform(trainX)
testX = encoder.transform(testX)

rank=8
n_iter=100

clf = FMRegression(rank=rank, n_iter=n_iter)
clf.fit(trainX, trainY)
pred = clf.predict(testX)

print pred[0:100]
print np.rint(pred[0:100])
#print testY[0:50]


print np.mean((testY - pred) ** 2) ** 0.5
print accuracy_score(testY, np.rint(pred))


