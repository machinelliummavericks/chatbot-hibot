from .logic import LogicAdapter
from chatbot.conversation import Statement
from textblob.classifiers import NaiveBayesClassifier
from datetime import datetime
from geopy import geocoders


class TimeLogicAdapter(LogicAdapter):
    """
    The TimeLogicAdapter returns the current time.
    """

    def __init__(self, **kwargs):
        super(TimeLogicAdapter, self).__init__(**kwargs)

        training_data = [
            ("what time is it", 1),
            ("do you know the time", 1),
            ("do you know what time it is", 1),
            ("what is the time", 1),
            ("do you know the time", 0),
            ("it is time to go to sleep", 0),
            ("what is your favorite color", 0),
            ("i had a great time", 0),
            ("what is", 0)
        ]

        self.classifier = NaiveBayesClassifier(training_data)

    def process(self, statement, tag_processing = None):

        user_input = statement.text.lower()
        if "time" not in user_input:
            return 0, Statement("")

        try:
            # Find the time zone of the user based on latitude and longitude to get the correct time
            g          = geocoders.GoogleV3()
            user       = tag_processing.user
            lat,lon    = user.get_latitude_longitude()
            timezone   = g.timezone((lat,lon))

            now = datetime.now(timezone)

            confidence = self.classifier.classify(user_input)
            response = Statement("The current time is " + now.strftime("%I:%M %p"))
        except:
            confidence = self.classifier.classify(user_input)
            response = Statement("Sorry. I cannot find the current time. Possible bad user location based on latitude and longitude. Please try again later")

        return confidence, response
