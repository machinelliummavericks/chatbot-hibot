from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from chatbot import ChatBot

### START RUNNING WITH
### > sudo mongod

# Create a new instance of a ChatBot
chatbot = ChatBot("Terminal", read_only=True,
    storage_adapter="chatbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapters=[
        "chatbot.adapters.logic.AttributeLogicAdapter",
        "chatbot.adapters.logic.TimeLogicAdapter",
        "chatbot.adapters.logic.WeatherLogicAdapter",
        "chatbot.adapters.logic.MovieLogicAdapter",
        "chatbot.adapters.logic.ClosestMatchAdapter"
    ],
    io_adapter="chatbot.adapters.io.TerminalAdapter",
    pyowm_api_key="cf798079c1e5c638a93cc16cff6d7171",
    #user_profile="user.pkl",
    database="chatterbot-database")

'''
chatbot.train("chatbot.corpus.english.overview")
chatbot.train("chatbot.corpus.english.greetings")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.atomic")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.atomic-categories0")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.knowledge")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.ai")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.astrology")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.biography")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.computers")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.emotion")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.geography")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.misc")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.music")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.politics")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.psychology")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.sports")
chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.science")
'''
user_input = "Type something to begin...\n"

print(user_input)

'''
In this example we use a while loop combined with a try-except statement.
This allows us to have a conversation with the chat bot until we press
ctrl-c or ctrl-d on the keyboard.
'''

while True:
    try:
        '''
        ChatBot's get_input method uses io adapter to get new input for
        the bot to respond to. In this example, the TerminalAdapter gets the
        input from the user's terminal. Other io adapters might retrieve input
        differently, such as from various web APIs.
        '''
        user_input = chatbot.get_input()

        '''
        The get_response method also uses the io adapter to determine how
        the bot's output should be returned. In the case of the TerminalAdapter,
        the output is printed to the user's terminal.
        '''

        #bot_input = chatbot.get_response(user_input)
        user_location = "latitude:42.1386410 longitude:-71.2474770"   #Walpole
        #user_location = "latitude:17.3850 longitude:78.4867"         #Hyderabad
        bot_input = chatbot.get_response(user_input, user_location)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

