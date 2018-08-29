from app.models import User
import unittest

class TestUsers(unittest.TestCase):

    # Set up basic user for testing
    def setUp(self):
        self.u = User(email="tom@test.com", username="tom", total_votes=0, plus_votes=0)

    def test_existance_user(self):
        self.assertTrue(self.u is not None)

    # Assert user info is properly set
    def test_set_info(self):
        self.assertTrue(self.u.email == "tom@test.com" and self.u.username == "tom" )

    def test_set_password(self):
        self.u.set_password = "petrocklover22"
        self.assertFalse(self.u.check_password("petrockhater66"))
        self.assertTrue(self.u.check_password("petrocklover22"))

    def test_add_rating(self):
        for i in range (1,4):
            self.u.add_rating(3 % i == 0)

        self.assertTrue(self.u.total_votes == 3)
        self.assertTrue(self.u.plus_votes == 2)
        self.assertTrue(self.u.show_rating() == 'Positive')


    def test_adjust_rating(self):
        for i in range (1,4):
            self.u.add_rating(3 % i == 0)

        self.u.adjust_rating(True)
        self.assertTrue(self.u.total_votes == 3)
        self.assertTrue(self.u.plus_votes == 1)
        self.assertTrue(self.u.show_rating() == 'Neutral')


    def test_rating_colors(self):
        self.assertTrue(self.u.rating_color('Untrustworthy') == 'danger')
        self.assertTrue(self.u.rating_color('Flaky') == 'warning')
        self.assertTrue(self.u.rating_color('Neutral') == 'info')
        self.assertTrue(self.u.rating_color('Positive') == 'info')
        self.assertTrue(self.u.rating_color('Praiseworthy') == 'success')
