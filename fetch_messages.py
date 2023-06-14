from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the SQLALCHEMY_DATABASE_URI from environment variables
DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

# Create engine
engine = create_engine(DATABASE_URI)

# Reflect the tables
metadata = MetaData()
metadata.reflect(bind=engine)

# Get the message table
Message = metadata.tables['message']  # Assuming 'message' is the name of your table

# Start a new session
Session = sessionmaker(bind=engine)
session = Session()

# Fetch all records
messages = session.query(Message).all()

# Print all records
for message in messages:
    print(f"ID: {message.id}, Body: {message.body}, Sender: {message.sender}")
