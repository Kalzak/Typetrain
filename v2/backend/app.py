from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from config import Config
from models import db, bcrypt, User, Text
from flask_cors import CORS
import random
import jwt as actual_jwt
import dbmodule

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Signup route
@app.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409

    new_user = User(
        username=username,
        password=User.hash_password(password)
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Protected route to get current user
@app.route('/user', methods=['GET'])
@jwt_required(optional=True)
def get_user():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({'user': current_user}), 200
    else:
        return jsonify({'user': 'Guest'}), 200

@app.route('/submittext', methods=['POST'])
@jwt_required()
def submit_text():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data.get('text') or len(data['text'].strip()) == 0:
        return jsonify({'message': 'Text cannot be empty'}), 400
    
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    new_submission = Text(text=data['text'], submitter_id=user.id)
    db.session.add(new_submission)
    db.session.commit()

    return jsonify({'message': 'Text suggestion submitted successfully'}), 201

@app.route('/randomtext', methods=['GET'])
def random_text():
    num_texts = Text.query.count()
    if num_texts == 0:
        return jsonify({'message': 'No texts found'}), 404
    random_offset = random.randint(0, num_texts - 1)
    random_text = Text.query.offset(random_offset).first()
    return jsonify({'text': random_text.text}), 200

@app.route('/mytexts', methods=['GET'])
@jwt_required()
def get_user_texts():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    texts = Text.query.filter_by(submitter_id=user.id).all()
    return jsonify({
        'texts': [
            {'id': text.id, 'text': text.text} for text in texts
        ]
    })

@app.route('/deletetext/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_text(id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    text = Text.query.filter_by(id=id, submitter_id=user.id).first()
    if not text:
        return jsonify({'message': 'Text not found'}), 404

    db.session.delete(text)
    db.session.commit()

    return jsonify({'message': 'Text deleted successfully'}), 200

def validate_jwt(token):
    try:
        decoded = actual_jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=[app.config['JWT_ALGORITHM']]
        )
        print("Decoded jwt:", decoded)
        return decoded
    except Exception as e:
        print("Error decoding jwt:", e)
        return None

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created before running the app
    app.run(debug=True)
