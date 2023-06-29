import os
import re
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Function to validate message
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

# Filtering the messages based on the rules
filtered_messages = []
for message in messages:
    message_body = message.body
    if is_valid_message(message_body):
        filtered_messages.append([message.id, message_body])

# Create a pandas dataframe
df = pd.DataFrame(filtered_messages, columns=['id', 'body'])

# Splitting the 'body' into separate columns
df[['date', 'student', 'subject', 'topic', 'time']] = df['body'].str.split(',', expand=True)

# Saving to CSV
df.to_csv('/home/hedhs/text_progress_tracker/cleaned_messages.csv', index=False)
print("CSV file has been created successfully.")
