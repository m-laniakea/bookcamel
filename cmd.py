#!/usr/bin/env python

## 
# High-level control module
#
# Usage hints: "./cmd.py <command> --help"
# or      "python cmd.py <command> --help"
#
# Launch this application in Python virtual environment 2.7 for proper 
# functionality.  
#
# Currently this application depends on ** sqlite **
#
# Dependencies are to be installed with:
#		pip install -r reqs.txt
##

import os
from app import create_app, db
from app.models import User, Book, Conversation, Message, Vote
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell

# Create app using default configuration from cfg.py
app = create_app(os.getenv('RUN_MODE') or 'default')

# Set up migrate for db operations
migrate = Migrate(app, db)

# Set up CLI interface
manager = Manager(app)

def shell_context():
    return dict(app=app, db=db, Book=Book, User=User, Conversation=Conversation, Message=Message, Vote=Vote)


# Define CLI commands
manager.add_command("shell", Shell(make_context=shell_context))
manager.add_command("db", MigrateCommand)

@manager.command
def test():
    import unittest, coverage
    cover = coverage.coverage(include='app/*', branch = True)
    cover.start()

    tests = unittest.TestLoader().discover('app/test')
    unittest.TextTestRunner(verbosity=3).run( tests )

    cover.stop()
    cover.save()
    cover.report()

if __name__ == '__main__':
    manager.run()


    


