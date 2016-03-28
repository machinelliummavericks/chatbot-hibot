from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from chatbot import ChatBot

bot = ChatBot("Math & Time Bot", read_only=False,
        logic_adapters=[
            "chatbot.adapters.logic.TimeLogicAdapter",
            "chatbot.adapters.logic.WeatherLogicAdapter",
            "chatbot.adapters.logic.ClosestMatchAdapter"
        ],

        io_adapter="chatbot.adapters.io.NoOutputAdapter",
        pyowm_api_key="cf798079c1e5c638a93cc16cff6d7171",
        database="database_weather.db"
)

response = bot.get_response("")

response = bot.get_response("whats the weather")
print("\n"+response)

response = bot.get_response("what time is it")
print("\n"+response)

response = bot.get_response("whats the weather in Boston today")
print("\n"+response)

'''
response = bot.get_response("whats my forecast")
print("\n"+response)

response = bot.get_response("whats the weather around me")
print("\n"+response)

response = bot.get_response("whats the extended weather around me")
print("\n"+response)

response = bot.get_response("whats the weather tomorrow")
print("\n"+response)

response = bot.get_response("whats the extended weather in Boston today")
print("\n"+response)

response = bot.get_response("check the weather in Boston")
print("\n"+response)

response = bot.get_response("whats the weather in Boston today")
print("\n"+response)

response = bot.get_response("whats the weather in New York today")
print("\n"+response)

response = bot.get_response("whats the weather in London today")
print("\n"+response)

response = bot.get_response("whats the weather in Londossn today")
print("\n"+response)

response = bot.get_response("whats the weather in aaa today")
print("\n"+response)
'''
