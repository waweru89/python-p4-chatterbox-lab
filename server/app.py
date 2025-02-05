from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)  # Enable Cross-Origin Resource Sharing
migrate = Migrate(app, db)  # Set up Flask-Migrate

db.init_app(app)  # Initialize the database with Flask app

# Route to get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()  # Get messages ordered by created_at
    return jsonify([message.to_dict() for message in messages])  # Return messages as JSON

# Route to get a specific message by id
@app.route('/messages/<int:id>', methods=['GET'])
def get_message(id):
    message = Message.query.get_or_404(id)  # Get message by ID or 404 if not found
    return jsonify(message.to_dict())  # Return the message as JSON

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()  # Get data from the request body
    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(new_message)  # Add the new message to the session
    db.session.commit()  # Commit changes to the database
    return jsonify(new_message.to_dict()), 201  # Return the new message as JSON with status 201

# Route to update a message by id
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.get_json()  # Get data from the request body
    message = Message.query.get_or_404(id)  # Get message by ID or 404 if not found
    message.body = data['body']  # Update the message body
    db.session.commit()  # Commit changes to the database
    return jsonify(message.to_dict())  # Return the updated message as JSON

# Route to delete a message by id
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)  # Get message by ID or 404 if not found
    db.session.delete(message)  # Delete the message from the session
    db.session.commit()  # Commit changes to the database
    return '', 204  # Return an empty response with status 204 (no content)

if __name__ == '__main__':
    app.run(port=5000)  # Run the Flask app on port 5555
