from models.base import Base, engine
from models.chat import Conversation, Message
from models.user import User

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db() 