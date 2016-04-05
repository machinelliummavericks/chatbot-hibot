from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from chatbot import ChatBot

bot = ChatBot("Movie Bot", read_only=False,
        logic_adapters=[
            "chatbot.adapters.logic.AttributeLogicAdapter",
            "chatbot.adapters.logic.TimeLogicAdapter",
            "chatbot.adapters.logic.MovieLogicAdapter",
            "chatbot.adapters.logic.ClosestMatchAdapter"
        ],

        io_adapter="chatbot.adapters.io.NoOutputAdapter",
        database="database_movie.db"
)

response = bot.get_response("")


question = "what movies are playing in Dallas"
print("\n[User]: " + question)
response = bot.get_response(question)
print(response)

question = "recommend a movie for me"
print("[User]: " + question)
response = bot.get_response(question)
print(response)


question = "learn my gender is female"
print("\n[User]: " + question)
response = bot.get_response(question)
print(response)

question = "learn my age is 42"
print("\n[User]: " + question)
response = bot.get_response(question)
print(response)


question = "recommend a movie for me"
print("\n[User]: " + question)
response = bot.get_response(question)
print(response)


MOnday - Integrated
Tuesday - Resolve
Wednesday - Demo full solutioun


