from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)  # Set up SQLAlchemy with metadata

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'  # Define the table name

    id = db.Column(db.Integer, primary_key=True)  # Message ID
    body = db.Column(db.String, nullable=False)  # Message content
    username = db.Column(db.String, nullable=False)  # Username of the sender
    created_at = db.Column(db.DateTime, default=db.func.now())  # Timestamp when the message is created
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())  # Timestamp when the message is updated
