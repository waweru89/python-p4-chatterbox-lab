#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")  # Ensure 'Duane' is included

def make_messages():
    Message.query.delete()  # Delete all existing messages in the database
    
    messages = []

    for i in range(20):
        message = Message(
            body=fake.sentence(),  # Generate a random sentence for the message body
            username=rc(usernames),  # Choose a random username from the list
        )
        messages.append(message)  # Add the message to the list

    db.session.add_all(messages)  # Add all messages to the session
    db.session.commit()  # Commit changes to the database

if __name__ == '__main__':
    with app.app_context():
        make_messages()  # Run the function to seed the database with fake data
