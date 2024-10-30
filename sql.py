from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import pandas as pd

load_dotenv()

## configure the generative AI model
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

## Function to load Gemini model
def get_gemini_response(input_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([prompt[0], input_text])
    return response.text

## Function to retrieve student data from SQLite database and return as DataFrame
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    data = pd.read_sql_query(sql, conn)
    conn.close()
    return data

prompt = ["""
You are an expert in converting English questions to SQL code.
The SQL database has the name students and has the following columns - NAME, CLASS, SECTION, and AGE

For example:
1. How many entries of records are present?
   The SQL command will be: SELECT COUNT(*) FROM students;

2. Find the average age of students in class 'B'.
   The SQL command will be: SELECT AVG(age) FROM students WHERE CLASS = 'B';

Ensure that the SQL code should not have *** in beginning or end and should not include the word 'sql' in the output.
"""]

## Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(f"Generated SQL Query: {response}")
    if response.strip():  # Check if the response is not empty
        try:
            query_result = read_sql_query(response, "student.db")
            st.subheader("The Response is:")
            st.write(query_result)  # Display the DataFrame in the app
        except Exception as e:
            st.error(f"Failed to execute query: {e}")
    else:
        st.error("Generated SQL query was empty, please check the input.")
