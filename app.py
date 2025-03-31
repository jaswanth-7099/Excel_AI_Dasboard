import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openai
# from config import OPENAI_API_KEY
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI API key set karo
openai.api_key = OPENAI_API_KEY

st.title("📊 AI-Powered Excel Chatbot")

# Excel file upload karo
uploaded_file = st.file_uploader("Upload Excel File (xlsx or csv)", type=["xlsx", "csv"])

# User ka question input lo
user_question = st.text_input("Ask a question about your data:")

if uploaded_file:
    # Excel ya CSV file ko read karo
    try:
        if uploaded_file.name.endswith("xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
    else:
        st.write("### 📋 Data Preview:")
        st.write(df.head())  # First 5 rows dikhao

        # Dashboard generate karo: Scatter plot & Histogram
        st.write("### 📊 Dashboard:")
        numeric_cols = df.select_dtypes(include=['number']).columns

        if len(numeric_cols) >= 2:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.scatterplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]], ax=ax)
            st.pyplot(fig)
        elif len(numeric_cols) > 0:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(df[numeric_cols[0]], kde=True, ax=ax)
            st.pyplot(fig)
        else:
            st.info("No numeric data available for dashboard charts.")

        # AI Summary generation using ChatGPT API
        def generate_summary(data):
            prompt = f"Analyze this data and provide key insights:\n{data.head().to_string()}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a data analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']

        st.write("### 📝 Summary:")
        summary = generate_summary(df)
        st.write(summary)

        # AI Chatbot: User ke question ka jawab data ke context mein
        def ask_chatgpt(question, data):
            prompt = f"Data:\n{data.head().to_string()}\n\nUser question: {question}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a data analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']

        if user_question:
            st.write("### 🤖 AI Response:")
            answer = ask_chatgpt(user_question, df)
            st.write(answer)
