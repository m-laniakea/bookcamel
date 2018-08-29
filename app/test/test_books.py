from app.models import Book, User
import unittest

class TestBooks(unittest.TestCase):

    def setUp(self):
        self.u1 = User(email = "e@m.com", username="HAL", id = 22)
        self.b = Book(title="A", author = "B", condition = 4, price = 22.22, isbn = 1234567890987, owner_id = self.u1.id)

    def test_book_info_integrity(self):
        c = self.b
        self.assertTrue(c.title=="A" and c.author == "B" and c.condition == 4 and c.price == 22.22 and c.isbn == 1234567890987)
        self.assertTrue(c.owner_id == 22 )


