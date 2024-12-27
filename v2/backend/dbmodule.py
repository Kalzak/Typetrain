from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import db, User, Text  # Reuse models.py
from config import Config
import random

# Set up SQLAlchemy engine and session factory
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

# Initialize models without Flask
db.metadata.create_all(bind=engine)

def get_random_text():
    session = Session()
    try:
        num_texts = session.query(Text).count()
        if num_texts == 0:
            return None
        random_offset = random.randint(0, num_texts - 1)
        random_text = session.query(Text).offset(random_offset).first()
        return random_text.text
    except Exception as e:
        raise DatabaseError
    finally:
        session.close()
