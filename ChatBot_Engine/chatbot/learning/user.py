from base_user import BaseUser

class User(BaseUser):
    """
    This class represents the attributes for all human HiBot users.
    """

    def __init__(self, **kwargs):
        self.name        = 'friend'
        self.age         = '30'
        self.gender      = 'male'
        self.location    = 'Boston'
        self.personality = 'great'
        self.job         = 'Physicists'
        self.intrests    = ['Comedy']
        #self.latitude    = '42.1386410'
        #self.longitude   = '-71.2474770'
        self.latitude    = '42.3601'
        self.longitude   = '-71.0589'

    def who_am_i(self):
        print "I am the user SFL"

    def get_name(self):
        return self.name
    def set_name(self, value):
        self.name = value

    def get_age(self):
        return self.age
    def set_age(self, value):
        self.age = value

    def get_gender(self):
        return self.gender
    def set_gender(self, value):
        self.gender = value

    def get_location(self):
        return self.location
    def set_location(self, value):
        self.location = value

    def get_personality(self):
        return self.personality
    def set_personality(self, value):
        self.personality = value

    def get_job(self):
        return self.job
    def set_job(self, value):
        self.job = value

    def get_intrests(self):
        return self.intrests
    def set_intrests(self, value):
        self.intrests = value

    def get_latitude_longitude(self):
        return self.latitude, self.longitude
    def set_latitude(self, latitude):
        self.latitude = latitude
    def set_longitude(self, longitude):
        self.longitude = longitude
    def set_latitude_longitude(self, latitude, longitude):
        self.latitude  = latitude
        self.longitude = longitude



