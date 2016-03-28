from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from chatbot import ChatBot

chatbot = ChatBot("HiBot", read_only = True,
    storage_adapter="chatbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapters=[
        "chatbot.adapters.logic.EvaluateMathematically",
        "chatbot.adapters.logic.TimeLogicAdapter",
        "chatbot.adapters.logic.ClosestMatchAdapter"
    ])

# Train based on the english corpus
#chatbot.train("chatbot.corpus.english")
chatbot.train("chatbot.corpus.english.greetings")
#chatbot.train("chatbot.corpus.english.conversations")
#chatbot.train("chatbot.corpus.english.trivia")

# Get a response to an input statement
chatbot.get_response("Hello I am a robot....@Qe3")


#chatbot.get_response("What time is it")
