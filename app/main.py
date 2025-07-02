# handling whitespace, invalid inputs, back/quit
import sqlite3
from chatbot import answer_query 
def page_divider():
    return str("- " * 50)

def get_animal_selection():
    dictionary = {
        "Wetlands": ["Cranes", "White-fronted Geese"],   #White-fronted_Geese
        "Forests": ["Red-backed Shrike", "White-crested Elaenia"],
        "Artic": ["Snowy Owls", "Ringed Seals"], 
        "Marine": ["Loggerhead Sea Turtles", "Common Terns", "Caspian Terns"]
    }
    return dictionary
def start_page():
    print(page_divider())
    print("Welcome to Animal Migration Explorer!")
    prompt = "press s to start or q to terminate the program:  "
    user_input = input(prompt).lower().strip()
    
    valid_input = ["s", "q"]
    while user_input not in valid_input:
        user_input = input(prompt).lower().strip()
    
    if user_input == "s":
        print("Valid commands: s to go to start page, q to quit, b to go back one page")
        choose_habitat()

    
    
def choose_habitat(): 
    print(page_divider())
    global valid_list_of_commands 
    valid_list_of_commands = ["s", "q", "b"]
    valid_habitats = list(get_animal_selection().keys()) 
    habitat_prompt = "What habitat are you interested in?\n - " + "\n - ".join(valid_habitats) + "\nType your answer below: \n"
    habitat = input(habitat_prompt).title().strip()
    

    while habitat not in valid_habitats and habitat.lower() not in valid_list_of_commands: 
        habitat = input(habitat_prompt).title().strip()

    if habitat.lower() == "s" or habitat.lower() == "b":
        start_page()
    elif habitat.lower() != "q":
        choose_animal(habitat)
    
    
def choose_animal(habitat):   
    print(page_divider())
    dictionary = get_animal_selection()
    prompt = "Select a "+ habitat +" animal:\n - " + "\n - ".join(dictionary[habitat]) + "\nType your answer below: \n"
    animal = input(prompt).lower().strip()
   
    lower_dictionary  = [x.lower() for x in dictionary[habitat]]
    
    while (animal not in lower_dictionary) and animal not in valid_list_of_commands:
        animal = input(prompt).lower().strip()

    i = lower_dictionary.index(animal)
    temp = dictionary[habitat][i]

    if animal.lower() == "s":
        start_page()
    elif animal.lower() == "b":
        choose_habitat()
    elif animal.lower() != "q": 
        get_article_info(temp,habitat)

def get_article_info(animal,habitat):
    print(page_divider())

    animal = animal.replace(" ", "_")
    #UPDATE PATH oF DB 
    conn = sqlite3.connect("../database/articles/articles.db")  
    cursor = conn.cursor()
    
    #White-fronted_Geese
    
    animal_query = f"SELECT * FROM '{animal}'"
    cursor.execute(animal_query)
    rows = cursor.fetchall()
    count = 1
    for url,summary in rows:
        print(f"Article {count}:")
        print(url)
        print(summary + "\n")
        count += 1
    #go back option 

    prompt = "Type m to generate a migration pattern map or c to access the chatbot:  "
    
    valid_input = ["m","c"]

    user_input = input(prompt).strip().lower()
   
    while user_input not in valid_input and user_input not in valid_list_of_commands:
        user_input = input(prompt).strip().lower()
      
    if user_input == "b":
        choose_animal(habitat)
    elif user_input == "s":
        start_page()
    elif user_input == "m":
        #map fun
        print("f")
    elif user_input == "c":
        chatbot(animal,habitat)
    

def chatbot(animal,habitat):
    valid = True
    while valid: 
        print(page_divider())
        query = input("Ask the chatbot a question: \n").strip()
        if query.lower() in valid_list_of_commands:
            valid  = False
            if query.lower() == "b":
                get_article_info(animal, habitat)
            elif query.lower() == "s":
                start_page()
            elif query.lower() == "q":
                break 
        
        print(answer_query(query))
    
   
if __name__ == "__main__":
    start_page()
