# Animal Migration Explorer

Animal Migration Explorer is an interactive program that combines data visualization through maps, curated articles, and real-time prompts to provide both visual and textual insights into migration patterns of animals. 

## Table of Contents
- [Preview](##Preview)
- [Technologies](##Technologies)
- [Setup and Run](##Setup/Run)

## Preview 
Below is a preview of some of the available features, including map generation and article recommendations.

- Map Generation (example with the common terns):  
![Map of the migration path of common terns from June 2011 to June 2012.](https://github.com/user-attachments/assets/b5939e77-a1cf-46e2-9172-792c40c8b2de)  
Map of the migration path of common terns from June 2011 to June 2012. 

- Article Summaries (example with the common terns):  
![List of links to and summaries of recommended articles about common terns.](https://github.com/user-attachments/assets/a630bb84-0c33-4dfd-ac17-ad0be27395c9)  
List of links to and summaries of recommended articles about common terns.  

## Technologies 
Language: 
- Python (version 3.XX+)

API: 
- MoveBank API (https://www.movebank.org/movebank/service/direct-read?entity_type=event&study_id={study_id}); requires username and password.
- Google GenAI API (model used: gemini-2.5-flash); free to use and no authentication required.

Database:
- SQL

## Setup/Run
To setup the program, run the following commands: 
```bash
git clone https://github.com/GabrielThrasher/Animal-Migration-Explorer.git
cd Animal-Migration-Explorer
pip install -r requirements.txt
```
Afterwards, to run the program, make sure you are in the `Animal-Migration-Explorer` directory and execute the command below.
```bash
python app.main {width} {margin}
```
where width and margin are both integers and are both optional parameters. Acceptable width values are between 60 and 200 and is the number of characters wide you want your program to be. Meanwhile, margin, like in a Word document, is the amount of spaces (in this case, characters) you want on the edge of your program before the words appear. Margin values that are allowed are between 2 and 5. If you do not specify parameters for either width or margin, then the non-specified parameter will be set to their default value: width at 100 and margin at 3.
