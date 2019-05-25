class Config(object):
    ''' General flask config '''
    DEBUG = False
    TESTING = False
    DB_NAME = "bec"

class TestingConfig(Config):
    ''' Testing Flask config '''
    TESTING = True

class DebugConfig(Config):
    ''' Debug Flask config '''
    DEBUG = True