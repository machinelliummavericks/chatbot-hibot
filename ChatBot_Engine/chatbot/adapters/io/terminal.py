from chatbot.adapters.io import IOAdapter
from chatbot.utils.read_input import input_function


class TerminalAdapter(IOAdapter):
    """
    A simple adapter that allows chatbot to communicate
    over the terminal.
    """

    def process_input(self):
        """
        Read the user's input from the terminal.
        """
        user_input = input_function()
        return user_input

    def process_response(self, statement):
        print("[ChatBot]: "+statement.text+"\n")
        return statement.text
