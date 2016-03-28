from chatbot.adapters.io import IOAdapter
from chatbot.utils.read_input import input_function


class NoOutputAdapter(IOAdapter):
    """
    The NoOutputAdapter is a simple adapter that
    doesn't display anything.
    """

    def process_input(self):
        """
        Read the user's input from the terminal.
        """
        user_input = input_function()
        return user_input

    def process_response(self, statement):
        return statement.text
