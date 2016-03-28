from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from chatbot import ChatBot

### START RUNNING WITH
### > sudo mongod

# Create a new instance of a ChatBot
chatbot = ChatBot("Terminal", read_only=False,
    storage_adapter="chatbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapters=[
        "chatbot.adapters.logic.AttributeLogicAdapter",
        "chatbot.adapters.logic.EvaluateMathematically",
        "chatbot.adapters.logic.TimeLogicAdapter",
        "chatbot.adapters.logic.WeatherLogicAdapter",
        "chatbot.adapters.logic.ClosestMatchAdapter"
    ],
    io_adapter="chatbot.adapters.io.TerminalAdapter",
    pyowm_api_key="cf798079c1e5c638a93cc16cff6d7171",
    user_profile="user.pkl",
    database="chatterbot-database")

#chatbot.train("chatbot.corpus.english.greetings")
#chatbot.train("chatbot.corpus.english.conversations")
#chatbot.train("chatbot.corpus.english.trivia")
#chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.atomic")

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
        ChatterBot's get_input method uses io adapter to get new input for
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
        bot_input = chatbot.get_response(user_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

