##
# Standard configuration file
##

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ##
    # Secret key used for cookies to validate user sessions
    ## Set SECRET_KEY environment variable before running on production 
    #
    # UNIX
    #  export SECRET_KEY="something long and random"
    #
    # WINDOWS
    #  set SECRET_KEY="something long and random"
    ##
    SECRET_KEY = os.getenv('SECRET_KEY') or 'b0b704bd28dbad2749d4a8d0f20c5972d7ec936e2eb52eb4f1f6bd1988e031036586defb184ca004bfe6ca5802187e557ad0b63b209238474ca12c6ac40057e5'

    # Automatically commit on db action
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RECAPTCHA_PUBLIC_KEY =  os.getenv('RECAPTCHA_KEY_PUBLIC')  or '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_KEY_PRIVATE') or '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'

    @staticmethod
    def init_app(app):
        pass

##
# Define various configurations to load
# Depending on environment
##
class devConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    
class testConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')

##
# Production Configuration
##
## NOT READY
class prodConfig(Config):
    SQL_ALCHEMY_DATABASE_URI = 'mysql://node@somesqlserver.com/db'
    
cfg = {
        'dev'  : devConfig,
        'test' : testConfig,
        'prod' : prodConfig,

        'default' : devConfig
}
