##
# Simple unit test to assert app 
# startup/shutdown sequence work as intended
#
# Recommend setting RUN_MODE env. variable to 'test'
# before testing with ./cmd test
##

from flask import current_app
from app import db, create_app
import unittest

class TestStartShutdown(unittest.TestCase):

    # Defines what to be run at the beginning of each test
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    # First test. Tests must begin with "test_"
    def test_startup(self):
        db.create_all()

    def test_correct_runmode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_existance(self):
        self.assertTrue(current_app is not None)
        
    def test_shutdown(self):
        db.session.remove()
        db.drop_all()


    # Define action to take at end of test
    def tearDown(self):
        self.app_context.pop()
      
