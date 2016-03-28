#from exceptions import UserNotImplementedError

class BaseUser(object):
    """
    This is an abstract class that represents the interface
    that all users should implement.
    """

    def who_am_i(self):
        """
        Returns basic information on type of User
        """
        #raise UserNotImplementedError()
        raise NotImplementedError



