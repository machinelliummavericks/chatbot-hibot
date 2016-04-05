from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from chatbot import ChatBot

bot = ChatBot(
    "Math & Time Bot",
    logic_adapters=[
        "chatbot.adapters.logic.EvaluateMathematically",
        "chatbot.adapters.logic.TimeLogicAdapter"
    ],
    io_adapter="chatbot.adapters.io.NoOutputAdapter",
)

# Print an example of getting one math based response
response = bot.get_response("What is 4 + 9?")
print(response)

# Print an example of getting one time based response
response = bot.get_response("What time is it?")
print(response)

# Print an example of getting one time based response
response = bot.get_response("do you know the time")
print(response)

# Print an example of getting one time based response
response = bot.get_response("i had a great time")
print(response)

# Print an example of getting one time based response
response = bot.get_response("it is time to go to sleep")
print(response)
