import sqlite3
import sys
import textwrap
from app.chatbot.chatbot import answer_query
from app.map_generation.generate_map import generate_map


class CLI:
    def __init__(self, program_char_width=0, page_char_margin=0):
        self.valid_list_of_commands = ["w", "q", "b"]
        if program_char_width < 60 or program_char_width > 200:
            self.program_char_width = 100
        else:
            self.program_char_width = program_char_width
        if page_char_margin < 2 or page_char_margin > 5:
            self.page_char_margin = 3
        else:
            self.page_char_margin = page_char_margin
        self.page_char_width = self.program_char_width - self.page_char_margin
        self.invalid_input_prefix = ">>>> INVALID INPUT -- PLEASE TRY AGAIN. "
        self.page_divider = "=" * self.program_char_width
        self.section_divider = "-" * (
                self.page_char_width - self.page_char_margin
        )
        self.page_edge = "|"
        self.animal_selection = {
            "Wetlands": 
                ["Cranes", "White-fronted Geese"],
            "Forests": 
                ["Red-backed Shrike", "White-crested Elaenia"],
            "Artic": 
                ["Snowy Owls", "Ringed Seals"],
            "Marine": 
                ["Loggerhead Sea Turtles", "Common Terns", "Caspian Terns"]
        }
        self.animal = None
        self.habitat = None
        self.chatbot_convo = ""
        self.program_running = True

    def get_title_header(self, title):
        title = (self.page_edge + " " + title + " " * 
                 (self.program_char_width - 2 * len(self.page_edge) - 
                  len(title) - 1) + self.page_edge)
    
        header = (
                self.page_divider + "\n" + title + "\n" +
                self.page_divider
        )
    
        return header
    
    def wrap_text(self, text, header=False, print_text=True,
                  separate_section=True, suffix=""):
        left_margin = self.page_edge + " " * (self.page_char_margin - 1)
        max_char_width = self.page_char_width
    
        if header:
            left_margin = ""
            max_char_width = self.program_char_width
    
        wrapped_text = "\n".join(textwrap.fill(
            line, width=max_char_width,
            initial_indent=left_margin, subsequent_indent=left_margin
        ) for line in text.splitlines())
    
        if not suffix:
            if not header:
                lines = wrapped_text.splitlines()
                for i, line in enumerate(lines):
                    right_margin = (
                            " " * (self.program_char_width - len(line) - 1) +
                            self.page_edge
                    )
                    lines[i] = line + right_margin
    
                wrapped_text = "\n".join(lines)
    
        else:
            wrapped_text += suffix
    
        if separate_section:
            wrapped_text = (
                    self.page_edge + " " * (
                    self.program_char_width - 2 * len(self.page_edge)
            ) + self.page_edge + "\n" + wrapped_text
            )
    
        if print_text:
            print(
                wrapped_text.encode('ascii', errors='ignore').decode()
            )
        else:
            return wrapped_text
        
    def wrap_page_divider(self):
        self.wrap_text(
            self.page_divider, header=True, separate_section=False
        )
        self.wrap_text("", header=True, separate_section=False)
    
    def wrap_header(self, title):
        self.wrap_page_divider()
        self.wrap_text(
            self.get_title_header(title), header=True, separate_section=False
        )
    
    def wrap_prompt(self, message):
        return input(self.wrap_text(
            message, print_text=False, suffix=" ")
        ).strip()
    
    def wrap_invalid_prompt(self, message):
        return input(self.wrap_text(
            self.invalid_input_prefix + message, print_text=False, suffix=" ",
            separate_section=False
        )
        ).strip()

    def get_options_format(self, options):
        options_str = ""
    
        for i, option in enumerate(options):
            options_str += f"{i + 1}. {option}\n"
    
        return options_str.strip()
    
    def is_in_range(self, str_num, upperbound, lowerbound=1):
        if not str_num.isdigit():
            return False
    
        int_num = int(str_num)
        if lowerbound <= int_num <= upperbound:
            return True
    
        return False

    def quit_page(self):
        self.wrap_header("Quit Page")
        self.wrap_text(
            "Thank you for using our program! Goodbye!", 
            separate_section=False
        )
        self.wrap_page_divider()
        self.program_running = False

    def welcome_page(self):
        self.wrap_header("Welcome Page")
        self.wrap_text(
            "Welcome to Animal Migration Explorer!", separate_section=False
        )
        self.wrap_text(
            "This is an interactive program that combines data visualization "
            "through maps, curated articles, and real-time prompts to provide "
            "both visual and textual insights into migration patterns of "
            "animals. To be able to access these features, you must first "
            "choose a habitat and animal within said habitat between the next "
            "two pages."
        )
        self.wrap_text(
            "For any prompt on future pages, the following commands will always"
            " be available for you to type in: 'w' to go to welcome page; 'b' "
            "to go back one page; 'q' to terminate the program."
        )
        self.wrap_text(
            "NOTE: This program is in beta, and as such the data available is "
            "limited to the given selections due to Movebank's API's "
            "animal-finding limitation."
        )
    
        prompt = "Type 's' to start or 'q' to terminate the program: "
        user_input = self.wrap_prompt(prompt).lower()
        
        valid_input = ["s", "q"]
        while user_input not in valid_input:
            user_input = self.wrap_invalid_prompt(prompt).lower()
        
        if user_input == "s":
            self.habitat_page()
        elif user_input == "q":
            self.quit_page()

    def habitat_page(self):
        self.wrap_header("Habitat Page")
    
        self.wrap_text(
            f"The following are the available habitats to choose from:",
            separate_section=False
        )
        habitat_options = list(self.animal_selection.keys())
        self.wrap_text(self.get_options_format(habitat_options))
    
        prompt = "Type in the number corresponding to the habitat:"
        user_input = self.wrap_prompt(prompt).lower()
    
        while (not self.is_in_range(user_input, len(habitat_options)+1) and 
               user_input not in self.valid_list_of_commands):
            user_input = self.wrap_invalid_prompt(prompt).lower()
    
        if user_input == "w":
            self.welcome_page()
        elif user_input == "b":
            self.welcome_page()
        elif user_input == "q":
            self.quit_page()
        else:
            self.habitat = habitat_options[int(user_input)-1]
            self.animal_page()
        
    def animal_page(self):
        self.wrap_header("Animal Page")
    
        self.wrap_text(
            f"The following are the available {self.habitat.lower()} "
            f"animals to choose from:", separate_section=False
        )
        animal_selection = self.animal_selection[self.habitat]
        self.wrap_text(self.get_options_format(animal_selection))
    
        prompt = f"Type in the number corresponding to the animal:"
        user_input = self.wrap_prompt(prompt).lower()
    
        while (not self.is_in_range(user_input, len(animal_selection)+1) and 
               user_input not in self.valid_list_of_commands):
            user_input = self.wrap_invalid_prompt(prompt).lower()
    
        if user_input == "w":
            self.welcome_page()
        elif user_input == "b":
            self.habitat_page()
        elif user_input == "q":
            self.quit_page()
        else:
            self.animal = animal_selection[int(user_input)-1]
            self.article_page()

    def article_page(self):
        self.wrap_header("Article Page")
    
        self.wrap_text(
            f"The following are links to and summaries about the "
            f"recommended reads for {self.animal.lower()}.",
            separate_section=False
        )
    
        animal_table = self.animal.replace(" ", "_")
        conn = sqlite3.connect("./database/articles.db")
        cursor = conn.cursor()
        animal_query = f"SELECT * FROM '{animal_table}'"
        cursor.execute(animal_query)
        rows = cursor.fetchall()
    
        for i, (url, summary) in enumerate(rows):
            self.wrap_text(f"Article {i+1}:")
            self.wrap_text(url)
            self.wrap_text(summary)

        prompt = ("Type 'm' to generate a migration pattern map or 'c' to "
                  "access the chatbot:")

        user_input = ""
        while (user_input not in self.valid_list_of_commands and
               self.program_running):
            user_input = self.wrap_prompt(prompt).lower()
            valid_input = ["m", "c"]
            while (user_input not in valid_input and user_input not in
                   self.valid_list_of_commands):
                user_input = self.wrap_invalid_prompt(prompt).lower()

            if user_input == "b":
                self.animal_page()
            elif user_input == "w":
                self.welcome_page()
            elif user_input == "q":
                self.quit_page()
            elif user_input == "m":
                save_path = generate_map(
                    self.animal.replace(" ", "_"),
                    "./database/coordinates.db",
                    save_dir="./app/map_generation/saved_maps/"
                )
                self.wrap_text("Generated and saved the migration pattern map "
                               f"at {save_path}.")
            elif user_input == "c":
                self.chatbot_page()
        
    def chatbot_page(self):
        self.wrap_header("Chatbot Page")
    
        self.wrap_text(
            f"Ask any {self.animal.lower()}-related questions to the "
            f"chatbot below. Remember, to leave the page type 'b'. Type 's' "
            f"to save you conversation with the chatbot to a file (end the "
            f"program to view its most recent contents).",
            separate_section=False
        )

        self.chatbot_convo = ""
        user_input = ""
        while (user_input not in self.valid_list_of_commands and
               self.program_running):
            self.wrap_text(self.section_divider)
            prompt = "Type here:"
            user_input = self.wrap_prompt(prompt)
    
            if user_input.lower() in self.valid_list_of_commands:
                if user_input == "b":
                    self.article_page()
                elif user_input == "w":
                    self.welcome_page()
                elif user_input == "q":
                    self.quit_page()

                break

            elif user_input.lower() == "s":
                chatbot_dir = "./app/chatbot/"
                convo_file_path = chatbot_dir + "chatbot_convo.txt"
                with open(convo_file_path, "w") as file:
                    file.write(self.chatbot_convo.strip())
                self.wrap_text(
                    f"Conversation saved successfully at {convo_file_path}."
                )

            else:
                self.chatbot_convo += "\n\n" + "YOU ASKED:" + "\n" + user_input
                response = answer_query(user_input)
                self.chatbot_convo += (
                        "\n" + "-" * 150 + "\n" + "CHATBOT ANSWERED:" + "\n" +
                        response + "\n" + "=" * 200
                )
                self.wrap_text(response)
    
   
if "__main__" == __name__:
    if len(sys.argv) == 1:
        cli = CLI()
    else:
        all_digits = True
        for arg in sys.argv[1:]:
            if not arg.isdigit():
                all_digits = False

        if all_digits:
            cli = CLI(*list(map(int, sys.argv[1:min(len(sys.argv), 3)])))
        else:
            cli = CLI()

    cli.welcome_page()
