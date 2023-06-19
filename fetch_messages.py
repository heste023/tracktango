import re
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import pandas as pd 

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

# Validation function
def is_valid_message(body):
    elements = body.split(',')

    if len(elements) != 5:
        return False
    
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    capital_letter_pattern = r'^[A-Z]$'
    word_or_pe_pattern = r'^[A-Za-z]+|PE$'
    duration_pattern = r'^\d+\s(minutes|hour|hours)$'

    if not re.match(date_pattern, elements[0].strip()):
        return False
    if not re.match(capital_letter_pattern, elements[1].strip()):
        return False
    if not re.match(word_or_pe_pattern, elements[2].strip()):
        return False
    if not re.match(duration_pattern, elements[4].strip()):
        return False
    
    return True

# Fetch all records
query = session.query(Message).statement
df = pd.read_sql(query, session.bind)

# Apply the validation function to the 'body' column to filter valid messages
df = df[df['body'].apply(is_valid_message)]

# Remove 'sender' column
df = df.drop(columns='sender')

# Print the DataFrame
print(df)
