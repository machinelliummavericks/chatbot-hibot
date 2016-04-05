from .logic import LogicAdapter
from chatbot.conversation import Statement
from chatbot.utils.pos_tagger import POSTagger
from textblob.classifiers import NaiveBayesClassifier
import nltk
import pyowm
from geopy.geocoders import Nominatim
import requests
import json
import datetime
from datetime import date, timedelta
import urllib2
from chatbot.learning.user import User

class WeatherLogicAdapter(LogicAdapter):
    """
    A logic adapter that returns information regarding the weather and
    the forecast for a specific location. Currently, only basic information
    is returned, but additional features are planned in the future.
    """

    def __init__(self, **kwargs):
        super(WeatherLogicAdapter, self).__init__(**kwargs)

        self.tagger = POSTagger()
        self.pyowm_api_key = kwargs.get("pyowm_api_key")
        self.DAYS = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}

        ## Train a classifier to recognize when a user is asking for the weather forecast
        ## around them or for a particular area.
        ## Data labeled with `1` is for around user, label with `0` is for particular area.
        training_data = [
                ("get the weather", 1),
                ("get weather", 1),
                ("what is the weather", 1),
                ("what's the weather", 1),
                ("tell me the weather", 1),
                ("do you know the weather", 1),
                ("get the forecast", 1),
                ("get forecast", 1),
                ("what is the forecast", 1),
                ("what's the forecast", 1),
                ("tell me the forecast", 1),
                ("do you know the forecast", 1),
                ("around me", 1),
                ("my weather", 1),
                ("my forecast", 1),
                ("my extended weather", 1),
                ("my extended forecast", 1),
                ("check the weather", 1),
                ("check the forecast", 1),

                ("weather in", 0),
                ("weather for", 0),
                ("what is the weather in", 0),
                ("what is the weather for", 0),
                ("forecast in", 0),
                ("forecast for", 0),
                ("what is the forecast in", 0),
                ("what is the forecast for", 0),
                ("check the weather in", 0),
                ("check the forecast in", 0),
            ]

        self.classifier = NaiveBayesClassifier(training_data)


    def process(self, statement, tag_processing = None):
        """
        Returns the forecast for a location (using location).
        """
        ## Cannot pass lower case text into Entity Extractor so keep two versions
        user_input_to_check = statement.text.lower()
        user_input = statement.text
        if "weather" not in user_input_to_check and "forecast" not in user_input_to_check:
            return 0, Statement("")

        ## Check if user wants to know the 7-day forecast
        extended_forecast = False
        if "extended" in user_input_to_check or "tomorrow" in user_input_to_check:
            extended_forecast = True

        ## Check if user wants to know the weather around them
        around_me_confidence = self.classifier.classify(user_input_to_check)
        around_me = False
        #if "around me" in user_input_to_check:
        if around_me_confidence == 1:
            around_me = True

        ## Get the current latitude and longitude of the user based on IP
        if around_me:
            user       = tag_processing.user
            lat,lon    = user.get_latitude_longitude()
            user_input = self.get_user_location(lat,lon)
            #user_input = self.get_user_location()

        location = self.get_location(user_input)

        if location == "BAD LOCATION":
            return 1, Statement("Cannot find forecast for requested City/State/Country. Please check the spelling")
        if location is not "":
            # @TODO: Add more options for getting weather. This could include
            #   the current temperature, the current cloud cover, etc.
            try:
                return 1, Statement(self.build_output(location,extended_forecast))
            except:
                return 1, Statement("Cannot find forecast for " + location + ". Please try again.")

        return 0, Statement("")


    def build_output(self, location, extended_forecast):
        """
        Build string output to display
        """
        _str = ""
        if extended_forecast:
            _str = "The 7-day forecast in " + location + " is: "
            forecast = self.get_extended_weather(location)

            i = 1
            for o in forecast.get_forecast():
                #_str = _str +  "\n\t" + "Day " + str(i) + ": High = " + str(o.get_temperature('fahrenheit')['max']) + " Low = " + str(o.get_temperature('fahrenheit')['min'])
                DOW = (datetime.datetime.today() + timedelta(days=i)).weekday()
                _str = _str +  "\n\t" + str(self.DAYS[DOW]) + ": High = " + str(o.get_temperature('fahrenheit')['max']) + " Low = " + str(o.get_temperature('fahrenheit')['min'])
                i = i + 1
        else:
            _str = "The forecast in " + location + " is: " + str(self.get_weather(location)) + " Fahrenheit"

        return _str


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

    def get_user_location(self, lat=None, lon=None):
        """
        Returns the current location of the user.
        """
        #return json.load(urllib2.urlopen('http://ipinfo.io/json'))['city']
        geolocator = Nominatim()
        location = geolocator.reverse(str(lat)+","+str(lon))
        try:
            return location.raw['address']['town']
        except:
            return location.raw['address']['city']


    def get_latitude_longitude(self):
        """
        Returns the current latitude and longitude of the user.

        Do Not Use!
        """
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']

        return lat,lon

    def get_latitude(self, user_input):
        """
        Returns the latitude extracted from the input.
        """
        for token in self.tagger.tokenize(user_input):
            if "latitude=" in token:
                return re.sub("latitude=", "", token)

        return ""

    def get_longitude(self, user_input):
        """
        Returns the longitude extracted from the input.
        """
        for token in self.tagger.tokenize(user_input):
            if "longitude=" in token:
                return re.sub("longitude=", "", token)

        return ""

    def get_weather(self, location):
        """
        Returns the weather for a given location.
        """
        owm = pyowm.OWM(self.pyowm_api_key)
        observation = owm.weather_at_place(location)
        forecast = observation.get_weather()

        return forecast.get_temperature('fahrenheit')['temp']

    def get_extended_weather(self, location):
        """
        Returns the 7-day weather for a given location
        """
        owm = pyowm.OWM(self.pyowm_api_key)
        observation = owm.daily_forecast(location)

        return observation


