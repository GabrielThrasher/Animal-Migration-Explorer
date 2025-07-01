import os 
from google import genai
from google.genai import types
import sqlite3
import json 
from dotenv import load_dotenv 
import random 
import time

#Retrieve the API key from .env
load_dotenv()
API_key = os.getenv("API_key")

client = genai.Client(
    api_key=API_key,
)

#Function passes article text through API to generate article summary. 
def retrieve_summary(article_text): 
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
        system_instruction="Write 3 lines summarizing the provided text."
    ),
        contents=article_text,
    )

    return response.text 

#Reads the json file containing all of the article data. 
with open("article_data.json", "r") as file:
  article_data = json.load(file)

#Connect to the articles database. 
conn = sqlite3.connect('../articles.db')
cursor = conn.cursor()

animals = ["Cranes", "ForkTailedFlycatchers", "RedBackedShrike", "WhiteCrestedElaenia", "CommonTerns",
"CaspianTerns",
"LoggerheadSeaTurtles",
"SnowyOwls",
"WhiteFrontedGeese",
"RingedSeals"]

#Create tables named by each anima. 
def populate_table(animal): 
  
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {animal} (
      url TEXT,
      summary TEXT
    )
    """
    insert_query = f"INSERT INTO {animal} (url, summary) VALUES (?, ?)"
    cursor.execute(create_table_query)
    for url,data in article_data[animal].items():
        for attempt in range(5): 
            try: 
                summary = retrieve_summary(data)
            except Exception as e:
                wait = (2 ** attempt) + random.uniform(0, 1)
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait:.2f} seconds...")
                time.sleep(wait)

    
        cursor.execute(insert_query, (url, summary))
    conn.commit()


for animal in animals:
    populate_table(animal)

