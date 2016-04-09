from .logic import LogicAdapter
from chatbot.conversation import Statement
from textblob.classifiers import NaiveBayesClassifier
import nltk
from chatbot.learning.user import User

class AttributeLogicAdapter(LogicAdapter):
    """
    A logic adapter that determines if the user is telling the
    bot to learn something about themselves.

    For example: Learn my name is Mike
    """

    def __init__(self, **kwargs):
        super(AttributeLogicAdapter, self).__init__(**kwargs)


        ## Train a classifier to recognize when a user is asking the bot to Learn something
        ## Data labeled with `1` is for learning, label with `0` is not.
        training_data = [
                ("learn", 1),
                ("learn my", 1),
                ("learn my is", 1),

                ("my is", 0),
                ("what is", 0)
            ]

        self.classifier = NaiveBayesClassifier(training_data)


    def find_tag(self, statement):
        """
        Find which tag the user is tying to set
        """
        if 'name is' in statement:
            return 'name'
        elif 'age is' in statement:
            return 'age'
        elif 'gender is' in statement:
            return 'gender'
        elif 'location is' in statement:
            return 'location'
        elif 'personality is' in statement:
            return 'personality'
        elif 'job is' in statement:
            return 'job'
        else:
            return None

    def process(self, statement, tag_processing = None):
        """
        Sets an attribute for the user
        """
        ## Cannot pass lower case text into Entity Extractor so keep two versions
        user_input_to_check = statement.text.lower()
        user_input = statement.text
        if "learn" not in user_input_to_check:
            return 0, Statement("")

        ## Check if user wants to know the weather around them
        learn_confidence = self.classifier.classify(user_input_to_check)

        #if "Learn" in user_input:
        if learn_confidence == 1:
            ## If specific tag in user input, extract tag and update user
            tag = self.find_tag(user_input_to_check)
            if tag is not None:
                att = user_input.split("is ",1)[1]
                tag_processing.set_user_tags(tag, att)
                return 1, Statement("Ok, I Learned your " + tag + " is " + att)
            else:
                txt = "I didn't get that. Please use the exact syntax for one of the following options:\n\tLearn my name is (your name)\n\tLearn my age is (your age)\n\tLearn my gender is (your gender)\n\tLearn my location is (your location)\n\tLearn my personality is (your personality)\n\tLearn my job is (your job)"
                return 1, Statement(txt)

        else:
            return 0, Statement("")

