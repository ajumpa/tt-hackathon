
from urllib.parse import urljoin
import json
import re

from openai import OpenAI
import requests
import streamlit as st

def call_chat_completion(client, query, context, model_id, tt_base_url):

    system_message = {
        "role": "system",
        "content":
            f"""
            You are given a well known short story as a series of bytes. The user wants you to identify the main characters \n
            with the following information for each character\n

            'name', 'description', 'character traits'\n
            Here is the story\n

            {context}
            """
    }


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Who are the main characters?",
            }, 
            system_message
        ],
        model=model_id,
        max_tokens=400,
    )

    return  chat_completion.choices[0].message.content


LLAMA = "meta-llama/Llama-3.1-8B-Instruct"
TT_BASE_URL = "https://disciplinary-sibella-nayadaur-c5543355.koyeb.app/v1"
def main():
    st.title("Interactive Short Stories")
    st.caption("Chat with characters from your stories in real time!")

    client = OpenAI(base_url=TT_BASE_URL, api_key="null")
    models = client.models.list()

    ids = [m.id for m in models]
    if LLAMA in ids:
        model_id = LLAMA

    
    story_file = st.file_uploader("Add short story (.txt)!", type="txt")
    query = None
    if story_file:
      story_bytes_encode = story_file.read().decode('utf-8')  
      query = st.text_input("What would you like to ask about the story?", value="Who are the main characters?")

      with st.spinner("💬 Generating answer..."):

          response = call_chat_completion(client, query, story_bytes_encode, model_id, TT_BASE_URL)

          st.markdown("**Answer:**")
          st.write(response)

if __name__ == "__main__":
    main()