from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from chatbot import ChatBot

chatbot = ChatBot("HiBot", read_only=False,
    storage_adapter="chatbot.adapters.storage.JsonDatabaseAdapter",
    #storage_adapter="chatbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapters=[
        "chatbot.adapters.logic.AttributeLogicAdapter",
        "chatbot.adapters.logic.EvaluateMathematically",
        "chatbot.adapters.logic.WeatherLogicAdapter",
        "chatbot.adapters.logic.TimeLogicAdapter",
        "chatbot.adapters.logic.ClosestMatchAdapter"
    ],
    pyowm_api_key="cf798079c1e5c638a93cc16cff6d7171",
    database="chaerbot-database_test.db")

# Train based on the english corpus
#chatbot.train("chatterbot.corpus.english")
chatbot.train("chatbot.corpus.english.greetings")
#chatbot.train("chatbot.corpus.english.conversations")
chatbot.train("chatbot.corpus.english.trivia")
#chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.ai")
#chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.drugs")
#chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.sex")
#chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.atomic")
##chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.science")
#chatbot.train("chatbot.corpus.english.AIML.AIML_IN_JSON.misc")

'''
chatbot = ChatBot("HiBot", read_only=False,
    #storage_adapter="chatbot.adapters.storage.JsonDatabaseAdapter",
    storage_adapter="chatbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapters=[
        "chatbot.adapters.logic.AttributeLogicAdapter",
        "chatbot.adapters.logic.EvaluateMathematically",
        "chatbot.adapters.logic.WeatherLogicAdapter",
        "chatbot.adapters.logic.TimeLogicAdapter",
        "chatbot.adapters.logic.ClosestMatchAdapter"
    ],
    pyowm_api_key="cf798079c1e5c638a93cc16cff6d7171",
    database="chatterbot-database")
'''

## This is needed to create database if does not already exists
response = chatbot.get_response("")

#question = "WHO AM I"
#question = "do you like cats"
question = "Hello"
print("[User]: " + question)
chatbot.get_response(question)

'''
question = "Learn my name is Mike"
print("[User]: " + question)
chatbot.get_response(question)

question = "Learn my age is 25"
print("[User]: " + question)
chatbot.get_response(question)

question = "Learn my gender is Robot"
print("[User]: " + question)
chatbot.get_response(question)

question = "WHO AM I"
print("[User]: " + question)
chatbot.get_response(question)


#print("Saving user attributes to file...")
#chatbot.save_user_attributes(file_name = 'user.pkl')
'''

'''
# Get a response to an input statement
question = "I WAS TALKING TO YOU"
print("[User]: " + question)
chatbot.get_response(question)


question = "What is the weather in Boston"
print("[User]: " + question)
chatbot.get_response(question)


question = "What is the extended forecast in Dallas"
print("[User]: " + question)
#chatbot.get_response(question)

question = "What is the time"
print("[User]: " + question)
#chatbot.get_response(question)

question = "Good morning! How are you doing?"
print("[User]: " + question)
chatbot.get_response(question)

question = "WHAT ARE THE LAWS OF THERMODYNAMICS"
print("[User]: " + question)
chatbot.get_response(question)

question = "how did you know that?"
print("[User]: " + question)
chatbot.get_response(question)

question = "how"
print("[User]: " + question)
chatbot.get_response(question)

question = "how old is the earth"
print("[User]: " + question)
chatbot.get_response(question)

question = "you are very impressive"
print("[User]: " + question)
chatbot.get_response(question)

question = "you do not make any sense"
print("[User]: " + question)
chatbot.get_response(question)

question = "will you ever die"
print("[User]: " + question)
chatbot.get_response(question)

question = "who is your daddy?"
print("[User]: " + question)
chatbot.get_response(question)
'''
