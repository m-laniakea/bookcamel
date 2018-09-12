##
# Database definitions for SQLAlchemy
##

from . import db
from flask.ext.login import UserMixin
from . import login_manager 
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import random, os
from random import randint

##
# Table relating users and conversations
##
relations_table = db.Table('conversations_users', db.Model.metadata,
        db.Column('conversation_id', db.Integer, db.ForeignKey('conversations.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

##
# Class relating user voters & voted by
##
class Vote(db.Model):
    __tablename__ = 'votes'
    voted_for_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    voted_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    positive = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
##
# Users have:
# *one role_id 
# *many books
#
##  UserMixin provides:
#
#   is_authenticated()
#   is_anonymous()
#
#   get_id()    # Return user identifier 
##
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64), index=True)

    # Back-reference to multiple books the user will have
    books = db.relationship("Book", backref="owner", lazy="dynamic")

    user_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_online = db.Column(db.DateTime(), default=datetime.utcnow) 
    is_online = db.Column(db.Boolean, default=True)

    plus_votes = db.Column(db.Integer, default=0)
    total_votes = db.Column(db.Integer, default=0)

    conversations = db.relationship("Conversation", back_populates="participants", secondary=relations_table)

    @property
    def password(self):
        raise AttributeError('Unreadable Attribute')

    @password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    ##
    # Rating system based on the continuity-corrected Wilson score interval
    # https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval_with_continuity_correction
    # 
    # With z = 1.96, there is a 95% chance that the true rating lies between the upper and lower limit of the interval
    #
    #                  2np + z^2 -+ [z*sqrt(z^2 - 1/n + 4*n*p*(1-p) +- (4p-2)) + 1]
    # w_max, w_min =   ------------------------------------------------------------
    #                                         2(n + z^2)
    #
    # Our rating system depends on the center of this interval, which simplifies to the computationally less demanding:
    #
    #         2(positive_votes) + z^2
    # w_c =  -----------------------  where p = positive/total, n = total_votes
    #          2(total_votes + z^2)
    ##
    
    ##
    # Return a name describing the user's current rating
    ##
    def show_rating(self):
        if self.total_votes == 0:
            return "Unrated"

        name = ""
        # Here, z = 1.44 corresponds to 85% confidence
        rating = (self.plus_votes + 1.0368) / (self.total_votes + 2.0736)

        if rating >= 0.95:
            name = "Praiseworthy"
        elif rating >= 0.8:
            name = "Recommended"
        elif rating >= 0.595:
            name = "Positive"
        elif rating >= 0.4:
            name = "Neutral"
        elif rating >= 0.2:
            name = "Flaky"
        else:
            name = "Untrustworthy"

        return name

    ##
    # Return css style colour assosiated with user's rating
    ##
    def rating_color(self, name):
        colors = { 'Praiseworthy':'success', 'Recommended':'success', 'Positive':'info', 'Neutral':'info', 'Flaky':'warning', 'Untrustworthy':'danger', 'Unrated':'default' }

        return colors[name]
    

    ##
    # Add new rating to user
    ##
    def add_rating(self, plus_vote):
        self.total_votes += 1
        
        if plus_vote:
            self.plus_votes += 1
   ##
   # Adjust rating if already voted for
   ##
    def adjust_rating(self, old_positive):
        if old_positive:
           self.plus_votes -= 1
        else:
            self.plus_votes += 1


    # Define default representation of User
    def __repr__(self):
        return 'User %s "%s", rating: %s' % (self.username, self.email, self.show_rating())

    ##
    #
    ## POPULATE
    #
    # Initiate & Populate db with users,
    # randomly generated book titles
    #
    # Requires dct.txt dictionary
    ##
    @staticmethod
    def populate():

        # Get base directory for cross-system filepaths
        basedir = os.path.abspath(os.path.dirname(__file__))
        wordlist = [l.strip() for l in open(os.path.join(basedir, "dct.txt"))]

        emails = ["test@test.com", "test0@test.com", "test1@test.com", "test2@test.com", "test3@test.com"]
        unames = ["bruce", "cate", "bitfracture", "ruby", "aarongupta"]

        ## Populate db with user in the two lists, assign random rating
        for i in range(len(emails)):

            user = User(email = emails[i], username = unames[i], set_password = 'toor', 
                    total_votes=0, plus_votes=0, is_online=False, location="University of Washington")

            # Add random rating
            for j in range( randint(0, 13) ):
                tmp = True if randint(0,5) < 3 else False
                user.add_rating(tmp)


            db.session.add(user)


            ## Gen fake books with random names, 
            ## titles, prices, ISBNs, & conditions
            for j in range( randint(2, 8) ):
                book = Book(title = User.gen_placeholder(wordlist, randint(1,3)), owner=user, 
                        author = User.gen_placeholder(wordlist, 2), isbn = randint(0,9999999999999),
                        price = 0 if (randint(0,2) == 0 ) else randint(0,8888)/100.0, condition = randint(1,5))
                db.session.add(book)
        
        db.session.commit()

    # Return 1-n random words as a string
    @staticmethod
    def gen_placeholder(words, num_words):
        title = ""
        
        if num_words > 0:
            for i in range(num_words - 1): 
                title += random.choice(words).title() + " "

            title += random.choice(words).title() 

        return title

    ##
    # END POPULATE
    ##

##
# Books have:
# *one owner (Parent)
##
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=False, index=True)
    author = db.Column(db.String(128), unique=False, index=True)
    condition = db.Column(db.Integer, unique=False, index=True)
    price = db.Column(db.Float(precision=2, default=0))
    isbn = db.Column(db.BigInteger, unique=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return "\"%s\" by %s" % (self.title, self.author) 

##
# Conversations have:
# *two User as participants (Children) 
# *many messages
##
class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    participants = db.relationship("User", back_populates="conversations", secondary=relations_table)
    subject = db.Column(db.String(128))
    start_time = db.Column(db.DateTime(), default=datetime.utcnow)
    messages = db.relationship("Message", backref="conversation", lazy="dynamic")
    book_id = db.Column(db.Integer)

    def __repr__(self):
        return 'Topic \"%s\" with %s & %s' % (self.subject, self.participants[0], self.participants[1])

##
# Messages have:
# *One conversation as parent
##
class Message(db.Model):
    __tablename__= 'messages'
    id = db.Column(db.Integer, primary_key=True)
    send_time = db.Column(db.DateTime(), default=datetime.utcnow)
    sender = db.Column(db.String(64))
    contents = db.Column(db.String(256)) 
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))

    # Define default representation
    def __repr__(self):
        return "%s : %s" % (self.sender, self.contents)
