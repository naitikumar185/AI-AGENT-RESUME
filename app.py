#=======================LOAD MODULES========================

from  langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np

# To show web app:complete page layout
st.set_page_config(layout="wide")

#to give title 
st.title("AI RESUME MAKER")

st.write("""This app helps user to build customized Professional Resume with resume with latest job apply links""")

st.image("bg.png")
st.sidebar.title("Fill Important Details")
st.sidebar.image("bg.png")

GOOGLE_API_KEY = st.sidebar.text_input("Gemini-API",type="password")
GROQ_API_KEY = st.sidebar.text_input("Groq-API",type="password")
TAVILY_API_KEY = "st.sidebar.text_input("Tavily"-API",type="password")


model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)
# response =  model.invoke("Hello Buddy!")
# response.content[-1]['text']

def search_latest_news_jobs(query):
  """This function helps to fetch latest news or jobs related article using tavily"""

  client = TavilyClient(
      api_key = TAVILY_API_KEY)
  response = client.search(query)
  return response

  # Agent creation
agent = create_agent(
    model = model,
    tools =  [search_latest_news_jobs])

# agent

def main_agent(agent,query):
  """This is main agent , or leader agent orchestrate sub agents"""
  #giving prompt to create detailed prompt
  #for code generatioon

  prompt = """ You are AI assistant and below given detailed prompt for this .
     your task is to give detailed prompt for this .
     You are a professional Resume generator
     where user will give their personnal info ,
     you have to create detailed Resume
     for students or professionalnone ,
     it must be with dynamic UI and UX and ,
     with advanced CSS Professional Designing make sure to
     give output in HTML format only no markdowns allowed"""

  response = agent.invoke({'messages':[{'role':'user','content':prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text']

  # SAVE PROMPT USING FILE HANDLING

  with open ('prompt.txt','w') as f:
    f.write(detailed_prompt)

  user_details=f"""Below Given is a user details generate Resume based on that , if not
               given keep : default Resume:python developer user details:{query}"""

  final_prompt = prompt + detailed_prompt + user_details

  # Code generation
  response= agent.invoke({'messages':[{'role':'user','content':final_prompt}]})
  code = response['messages'][-1].content[-1]['text']

  return code

  #from IPython.display import display, HTML

#code = main_agent(agent, "Naitik Kumar , GEN AI EXPERT")
#display(HTML(code))


# Fetch Latest Domain related Jobs using Tavily
def get_jobs(agent,
             location="Noida,delhi",
             profile = "Data analysts , ai engineer"):
  Location = "Noida,Delhi"
  profile="Data Analysts,AI Engineer"

  prompt = """Based on user given job profile,
fetch latest jobs or job apply article
using Naukri, Linkedin, indeed, or all popular
Job apply platforms, Show Results with
JOB PROFILE NAME, LOCATION, SALARY, COMPANY NAME,
SHOW jobs only related to given
{Location} and {Profile}, output must be in
Professional HTML Naukri theme cards with Dynamic Design,
Show atleast Top 10-20 results with direct apply link"""

  response = agent. invoke({'messages':[{'role': 'user',
                                         'content': prompt}]})
  code = response['messages'][-1].content[-1]['text']

  return code
#code = get_jobs(agent)
#display(HTML(code))
