from .logic import LogicAdapter
from chatbot.conversation import Statement
from textblob.classifiers import NaiveBayesClassifier
import nltk
from chatbot.learning.user import User
from chatbot.utils.movie_parser import MovieShowtimes
from chatbot.learning.user import User
from chatbot.learning.recommender import Recommender
from chatbot.learning.segmentation import Segmentation
import pandas as pd
import numpy as np


class MovieLogicAdapter(LogicAdapter):
    """
    A logic adapter that returns information regarding surrounding movies.
    """

    def __init__(self, **kwargs):
        super(MovieLogicAdapter, self).__init__(**kwargs)

        ## Train a classifier to recognize when a user is asking about movies
        ## Data labeled with `1` is for movies, label with `0` is not.
        training_data = [
                ("movie", 1),
                ("whats playing", 1),
                ("my is", 0),
            ]

        self.classifier = NaiveBayesClassifier(training_data)
        self.recommender = 0
        self.cluster = 0

    def process(self, statement, tag_processing = None):
        """
        Returns the movies for a location (using location).

        @TODO: Need to work in something like Movies around me
        @TODO: Update training data
        @TODO: Fix time formatting
        """

        ## Cannot pass lower case text into Entity Extractor so keep two versions
        user_input_to_check = statement.text.lower()
        user_input = statement.text
        if "movie" not in user_input_to_check and "movies" not in user_input_to_check:
            return 0, Statement("")

        recommend = False
        if "recommend" in user_input_to_check:
            recommend = True


        if recommend:
            '''
            This path will use collaborative filtering to recommend a movie based on user demographics, interests, etc.
            '''
            user          = tag_processing.user
            user_age      = user.get_age()
            user_gender   = user.get_gender()
            user_interest = user.get_intrests()

            user_gender = ('M' if user_gender.lower() == 'male' else 'F')

            segmenation = False
            if segmenation:
                '''
                Perform customer segmentation to determine which cluster user belongs to
                @TODO: Hook this into recommendations, currently just returns cluster
                '''
                self.cluster = Segmentation()
                X = self.cluster.load_training_users()
                X_encoded = self.cluster.encode_train_data(X)
                self.cluster.load_model()

                ## Recommend movie for current user
                df_user = pd.DataFrame({'age':[int(user_age)], 'sex':[user_gender]})
                user_age_binary = self.cluster.get_age(df_user)
                user_gender_binary = self.cluster.get_gender(df_user)

                tmp = self.cluster.transform_new_data(np.array(np.concatenate(([99999,99999],user_age_binary,user_gender_binary))).reshape(1,-1))
                predicted_cluster = self.cluster.predict(tmp)[0]
                print "User cluster",predicted_cluster

            self.recommender = Recommender()
            X,y = self.recommender.load_training_users()
            X_encoded = self.recommender.encode_train_data(X)
            self.recommender.load_model()

            ## Recommend movie for current user
            df_user = pd.DataFrame({'age':[int(user_age)], 'sex':[user_gender]})
            user_age_binary = self.recommender.get_age(df_user)
            user_gender_binary = self.recommender.get_gender(df_user)

            movies_to_watch = {'Batman v Superman: Dawn of Justice': [99999,99999,user_age_binary,user_gender_binary,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
                               'Zootpia': [99999,99999,user_age_binary,user_gender_binary,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
                               'Whiskey Tango Foxtrot': [99999,99999,user_age_binary,user_gender_binary,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                               '10 Cloverfield Lane': [99999,99999,user_age_binary,user_gender_binary,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                               'The Revenant': [99999,99999,user_age_binary,user_gender_binary,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                               }
            movie_list = []
            ratings_list = []
            for movie in movies_to_watch:
                tmp = self.recommender.transform_new_data(np.array(movies_to_watch[movie]).reshape(1,-1))
                rating = self.recommender.predict(tmp)[0]
                movie_list.append(movie)
                ratings_list.append(rating)

            ratings_index = np.argsort(ratings_list)[::-1]

            str_cnt = 1
            top_movie_str = "\n"
            for i in ratings_index:
                top_movie_str = top_movie_str + "\t" + movie_list[i] + "\n"
                if str_cnt == 3:
                    break
                str_cnt = str_cnt + 1

            return 1, Statement("Based on what I know about you, the top 3 movies I recommend you seeing are" + top_movie_str)

        else:
            '''
            This path will simply display all the movies in a given area
            '''
            ## Check if user wants to know the weather around them
            learn_confidence = self.classifier.classify(user_input_to_check)

            #if "Learn" in user_input:
            if learn_confidence == 1:
                location = self.get_location(user_input)
                movies = MovieShowtimes(location,'','')
                movies = movies.parse()
                return 1, Statement(self.build_output(movies))
            else:
                return 0, Statement("")


    def build_output(self, movies, n_theaters = 3, n_movies = 5):
        """
        Build string output to display

        ## How many movie theaters and movies to display in output
        """

        movie_str = ""

        theater_cnt = 0
        for movie in movies['theater']:

            movie_str = movie_str + movie['name'] + "\n"
            movie_str = movie_str +  movie['info'] + "\n"

            movie_cnt = 0
            for m in movie['movies']:
                movie_str = movie_str +  "\t"+m['name'] + "\n"

                movie_times = [t for t in m['times'] if t!='']
                #movie_str = movie_str +  "\t"+m['info']+str(m['times']) + "\n"
                movie_str = movie_str +  "\t"+m['info']+str(movie_times) + "\n"
                movie_str = movie_str +  "\n"
                if movie_cnt == n_movies - 1:
                    break
                movie_cnt = movie_cnt + 1

            movie_str = movie_str + "\n"
            if theater_cnt == n_theaters - 1:
                break
            theater_cnt = theater_cnt + 1

        return movie_str


    def get_location(self, user_input):
        """
        Returns the location extracted from the input.
        """
        text = nltk.word_tokenize(user_input)
        nes = nltk.ne_chunk(nltk.pos_tag(text), binary=False)

        GPE = []
        for ne in nes:
            if hasattr(ne, 'label'):
                if (ne.label() == 'GPE') :
                    GPE.append(' '.join(c[0] for c in ne.leaves()))

        if len(GPE) > 0:
            return GPE[0]
        else:
            return "BAD LOCATION"


    def get_user_location(self):
        """
        Returns the current location of the user.
        """
        return json.load(urllib2.urlopen('http://ipinfo.io/json'))['city']



