from sentence_transformers import SentenceTransformer
import pinecone
import openai
import streamlit as st
from config import *
import snowflake.connector

# openai.api_key = openai_api_key
model = SentenceTransformer('all-MiniLM-L6-v2')

pinecone.init(api_key=api_key, environment=environment)
index = pinecone.Index(index_name)

# Define Snowflake connection parameters
conn = {
    "user"  : snowflake_user,
    "password": snowflake_password,
    "account": snowflake_account,
    "warehouse": snowflake_warehouse,
    "database": snowflake_database,
    "schema": snowflake_schema
}
# Create a Snowflake connection
connection = snowflake.connector.connect(**conn)


# Iterate through query history and insert into history_table  
def add_query_history(query):
    print(query)
    cursor = connection.cursor()
    insert_query = f"INSERT INTO history_table (history) VALUES ('{query}');"
    cursor.execute(insert_query)
    cursor.close()  

#Function to fetch query history from the history_table
def fetch_query_history():
    cursor = connection.cursor()
    query = "SELECT history FROM history_table"
    cursor.execute(query)
    history = [row[0] for row in cursor]
    cursor.close()
    return history

# # Function to check if the API key is valid
def is_valid_api_key(openai_api_key):
    return openai_api_key and openai_api_key.startswith('sk-') and len(openai_api_key) == 56

def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']


def query_refiner(conversation, query):
    response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text'] 

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string

