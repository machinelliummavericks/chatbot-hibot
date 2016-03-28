from base_user import BaseUser

class BotUser(BaseUser):
    """
    This class represents the attributes for HiBot chatbot.

    :example:
    user = User()
    print user.name
    user.name = 'Master Bot'
    print user.name
    user.who_am_i()

    user = User()
    string = "your name is name='name' and you are name='age'"
    #print user.name
    #setattr(user, 'name', 'mike')
    #print getattr(user, 'get_name')()
    #print "my name is " + getattr(user, 'get_name')()
    string = string.replace("name='name'",getattr(user, 'get_name')()).replace("name='age'",getattr(user, 'get_age')())
    print string
    """

    def __init__(self, **kwargs):
        self._name = 'HiBot'

    def who_am_i(self):
        print "I am the user master bot"

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

