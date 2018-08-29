from app.models import Vote, User
import unittest

class TestVotes(unittest.TestCase):

    def setUp(self):
        self.u1 = User(email="e@m.com", username = "HAL")
        self.u2 = User(email="f@o.com", username = "IBM")
        self.v = Vote(voted_for_id = self.u1.id, voted_by_id = self.u2.id, positive = True)


    def test_vote_existance(self):
        self.assertTrue(self.v is not None )

    def test_voter_id_integrity(self):
        self.assertTrue(self.v.voted_for_id == self.u1.id)
        self.assertTrue(self.v.voted_by_id == self.u2.id)

    def test_vote_cast_integrity(self):
        self.assertTrue(self.v.positive == True)


