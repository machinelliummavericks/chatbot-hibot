from user import User
from chatbot.conversation import Statement

class TagProcessing(object):
    """
    This class enables the ChatBot to process any tag found from AIML response with the corresponding user attribute.
    Also, it allows the Chatbot to learn new attributes that are passed in from the conversation.
    """

    def __init__(self, user, **kwargs):
        self.user = user

    def process_user_tags(self, statement):
        """
        Process any tag found with corresponding user attribute
        """
        statement = statement.replace("[get name='name']",       getattr(self.user, 'get_name')())\
                             .replace("[get name='age']",        getattr(self.user, 'get_age')())\
                             .replace("[get name='gender']",     getattr(self.user, 'get_gender')())\
                             .replace("[get name='location']",   getattr(self.user, 'get_location')())\
                             .replace("[get name='personality']",getattr(self.user, 'get_personality')())\
                             .replace("[get name='job']",        getattr(self.user, 'get_job')())

        return Statement(statement)

    def set_user_tags(self, tag, statement):
        """
        Set tag with corresponding user attribute
        """
        setattr(self.user, tag, statement)