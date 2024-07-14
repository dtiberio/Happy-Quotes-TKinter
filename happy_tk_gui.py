# Python

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import random

# Redirect stdout to the console_text widget while the TKinter mainloop is running
class RedirectedStdout:
    def __init__(self, widget):
        """
        Initialize the RedirectedStdout instance.
        
        Args:
            widget (ScrolledTextWidget): The widget to which stdout will be redirected.
        """
        self.widget = widget

    def write(self, message):
        """
        Write a message to the redirected stdout.
        
        Args:
            message (str): The message to write.
        """
        self.widget.insert_text(message)

    def flush(self):
        """
        Flush the output. This method is required for compatibility with Python's standard output.
        """
        pass

# Class for the ScrolledText Widget, this widget is used by the response_text and console_text widgets
class ScrolledTextWidget:
    def __init__(self, parent, **kwargs):
        """
        Initialize the ScrolledTextWidget instance.
        
        Args:
            parent (tk.Widget): The parent widget.
            **kwargs: Additional keyword arguments for the ScrolledText widget.
        """
        self.text_widget = scrolledtext.ScrolledText(parent, **kwargs)
        self.text_widget.pack(expand=True, fill="both", padx=10, pady=10)
        self._configure_tags()

    def _configure_tags(self):
        """
        Configure text tags for the ScrolledText widget.
        """
        self.text_widget.tag_configure("black")
        self.text_widget.tag_configure("bold", font=("Lucida Console", 12, "bold"))
        self.text_widget.tag_configure("red", font=("Lucida Console", 12, "bold"), foreground="red")
        self.text_widget.tag_configure("blue", font=("Lucida Console", 12, "bold"), foreground="blue")
        self.text_widget.tag_configure("green", font=("Lucida Console", 12, "bold"), foreground="green")
        self.text_widget.tag_configure("center", justify='center')

    def insert_text(self, text, *tags):
        """
        Insert text into the ScrolledText widget.
        
        Args:
            text (str): The text to insert.
            *tags: Tags to apply to the inserted text.
        """
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, text, tags)
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)
        
    def scroll_top(self):
        """
        Move the scrollbar to the top.
        """
        self.text_widget.yview_moveto(0.0)

    def get_widget(self):
        """
        Get the underlying text widget.
        
        Returns:
            scrolledtext.ScrolledText: The underlying text widget.
        """
        return self.text_widget

# This is the TKinter mainloop class, it includes the code for the program's View and Controller
class MyHappyGUI(tk.Tk):
    def __init__(self, model):
        """
        Initialize the MyHappyGUI instance.
        
        Args:
            model: The model instance to use for data operations.
        """
        super().__init__()
        
        self.model = model
        self.title("Happy Quotes")
        self.geometry("1400x750")

        # Creating the menu bar
        self.create_menu()

        # Creating the main frames
        self.create_main_frames()

        # Creating widgets for each section
        self.create_query_response_section()
        self.create_console_section()
        
        # Creating the footer section
        self.create_footer()

        # Set the default footer message
        self.default_footer_message()

        # Set event handler, when the user closes the window, execute on_closing()
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        # Store the original stdout, it is required later to restore it before exiting the main loop
        self.original_stdout = sys.stdout
        # Redirect stdout to console_text
        sys.stdout = RedirectedStdout(self.console_text)

        # Print the Welcome message
        self.print_welcome()

    def create_menu(self):
        """
        Create the menu bar for the application.
        """
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # 1. the Home menu
        home_menu = tk.Menu(menubar, tearoff=0)
        home_menu.add_command(label="Quit", command=self.on_closing)

        # 2. the Queries menu
        # the user interacts with the View by selecting a menu option
        # the View then calls the Presentation Controller (self.run_controller)
        # the Controller will call the Model and then will present the data to the user through updates to the View
        queries_menu = tk.Menu(menubar, tearoff=0)
        # requires a lambda funtion, to pass a reference to a function that will be called when the menu option is selected
        queries_menu.add_command(label=f"Select Quotes by Author", 
            command=lambda: self.run_controller('quotes_by_author'))
        
        queries_menu.add_command(label=f"Get X Random Quotes", 
            command=lambda: self.run_controller('x_quotes'))
        
        queries_menu.add_command(label=f"Get one Random Quote", 
            command=lambda: self.run_controller('random_quote'))
        
        queries_menu.add_command(label=f"Get total amount of Quotes", 
            command=lambda: self.run_controller('total_quotes'))
        
        queries_menu.add_command(label=f"Select Quotes by Tag", 
            command=lambda: self.run_controller('quotes_by_tag'))
        
        queries_menu.add_command(label=f"Get Top 5 Authors", 
            command=lambda: self.run_controller('top5_authors'))
        
        queries_menu.add_command(label=f"Get all the comments of Random Quote", 
            command=lambda: self.run_controller('comments_random_quote'))
        
        queries_menu.add_command(label=f"Get Author Bio", 
            command=lambda: self.run_controller('author_bio'))
        
        queries_menu.add_command(label=f"Get All Quotes", 
            command=lambda: self.run_controller('all_quotes'))
        
        queries_menu.add_command(label=f"Surprise !", 
            command=lambda: self.run_controller('surprise'))

        # 3. the Read Me and About menus
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Tutorial", command=self.show_tutorial)
        help_menu.add_command(label="About", command=self.show_about)

        # add the 3 menus to the menubar
        menubar.add_cascade(label="Home", menu=home_menu)
        menubar.add_cascade(label="Queries", menu=queries_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

    def create_main_frames(self):
        """
        Create the main frames for the application layout.
        """
        # 1. the Frame to display the results from the Queries
        self.query_response_frame = ttk.LabelFrame(self, text="Query response")
        self.query_response_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)

        # 2. the Frame to display status messages in the Console
        self.console_frame = ttk.LabelFrame(self, text="Console")
        self.console_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=6)

        # use the 'grid' method to have more control about placing the widgets
        # Configure grid weights for responsiveness
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=4)
        self.grid_columnconfigure(3, weight=4)
        self.grid_columnconfigure(4, weight=4)
        self.grid_columnconfigure(5, weight=4)

    def create_query_response_section(self):
        """
        Create the query response section widget.
        """
        # default state = DISABLED, the users can't edit content
        self.response_text = ScrolledTextWidget(self.query_response_frame, wrap=tk.WORD, height=30, state=tk.DISABLED)

    def create_console_section(self):
        """
        Create the console section widget.
        """
        self.clear_button = ttk.Button(self.console_frame, text="Clear", command=self.clear_console)
        self.clear_button.pack(anchor='w', padx=10, pady=10)
        self.clear_button.bind("<Enter>", lambda e: self.update_footer("Clear the console messages"))
        self.clear_button.bind("<Leave>", lambda e: self.default_footer_message())

        # default state = DISABLED, the user can't edit content
        self.console_text = ScrolledTextWidget(self.console_frame, wrap=tk.WORD, height=10, state=tk.DISABLED)

    def create_footer(self):
        """
        Create the footer section for the application.
        """
        self.footer = ttk.Label(self, text="", anchor="w")
        self.footer.grid(row=2, column=0, columnspan=6, padx=10, pady=5, sticky="ew")
        self.grid_rowconfigure(2, weight=0)
        
    def default_footer_message(self):
        """
        Set the default footer message.
        """
        python_version = sys.version.split(" ")[0]
        tkinter_version = tk.TkVersion
        self.footer.config(text=f"Happy Quotes, v0.5, 2024-06-28 | Python {python_version} | Tkinter {tkinter_version}")

    def update_footer(self, message):
        """
        Update the footer message.
        
        Args:
            message (str): The message to display in the footer.
        """
        self.footer.config(text=message)
    
    def print_welcome(self):
        """
        Print the welcome message in the console and response sections.
        """
        # Clear existing text
        self.clear_response()
        # Print Welcome text
        self.console_text.insert_text("Welcome!\nAll systems are GO!\n", 'black')
        self.response_text.insert_text("\n\n\nWELCOME TO HAPPY QUOTES!\n", 'bold', 'center')
        self.response_text.insert_text("\n\n\nWe hope you will enjoy this experience\nand find some inspiration to brighten your day!", 'blue', 'center')
        self.response_text.insert_text("\n\n\nStart at the 'Queries' menu.\nHave fun!\n", 'blue', 'center')
        # print the Quote Of The Day - qotd
        self.run_controller('qotd')

    def on_closing(self):
        """
        Handle the event when the user closes the window.
        """
        if messagebox.askyesno(title='Quit?', message='Do you really want to quit?'):
            sys.stdout = self.original_stdout   # restore stdout to the terminal
            self.destroy()    # if it's the main window, then it terminates the main loop

    def clear_console(self):
        """
        Clear the console text.
        """
        self.console_text.get_widget().config(state=tk.NORMAL)
        self.console_text.get_widget().delete("1.0", tk.END)
        self.console_text.get_widget().config(state=tk.DISABLED)

    def clear_response(self):
        """
        Clear the response text.
        """
        self.response_text.get_widget().config(state=tk.NORMAL)
        self.response_text.get_widget().delete('1.0', tk.END)
        self.response_text.get_widget().config(state=tk.DISABLED)

    def show_about(self):
        """
        Show the 'About' dialog.
        """
        messagebox.showinfo("About", "This is the Happy Quotes program,\n with quotes to brighten your day.\n")
    
    def show_tutorial(self):
        """
        Display the TUTORIAL.TXT file when the user selects the "Tutorial" menu option.
        """
        readme_window = tk.Toplevel(self)
        readme_window.title("TUTORIAL")

        text_widget = scrolledtext.ScrolledText(readme_window, wrap=tk.WORD, width=130, height=50)
        text_widget.pack(expand=True, fill=tk.BOTH)

        readme_path = 'TUTORIAL.TXT'
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as file:
                readme_content = file.read()
                text_widget.insert(tk.INSERT, readme_content)
        else:
            text_widget.insert(tk.INSERT, "TUTORIAL.TXT file not found.")

    def get_selection(self, items):
        """
        Show a list of items and return the selected item.
        
        Args:
            items (list): List of items to display.
            
        Returns:
            list: List of selected items.
        """
        self.selected_items = []

        def on_confirm():
            selected_indices = listbox.curselection()
            self.selected_items = [listbox.get(i) for i in selected_indices]
            popup.destroy()

        def on_cancel():
            self.selected_items = []
            popup.destroy()

        # Create a Toplevel window
        popup = tk.Toplevel(self)
        popup.title("Make Your Selection")
        popup.geometry("300x550")

        # Create and configure Listbox
        listbox_frame = tk.Frame(popup)
        listbox_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # set selectmode to SINGLE but alternatively could be MULTIPLE
        listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add items to Listbox
        for item in items:
            listbox.insert(tk.END, item)

        # Add a scrollbar
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        # Create buttons to confirm or cancel the selection
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        confirm_button = tk.Button(button_frame, text="Confirm", command=on_confirm)
        confirm_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        # Build the pop-up window and wait for it to close
        self.wait_window(popup)

        return self.selected_items

    def get_input(self):
        """
        Create a pop-up window to get input from the user.
        
        Returns:
            int: The user input value.
        """
        self.popup_value = None

        # build the window
        popup = tk.Toplevel(self)
        popup.title("Enter a number")

        label = tk.Label(popup, text="Please enter a number between 1 and 100:")
        label.pack(pady=10, padx=10)

        entry = tk.Entry(popup)
        entry.pack(pady=5, padx=5)

        def on_submit():
            try:
                value = int(entry.get())
                if 1 <= value <= 100:
                    self.popup_value = value
                    popup.destroy()
                else:
                    messagebox.showerror("Invalid Input", "Please enter a number between 1 and 100.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer number between 1 and 100.")

        submit_button = tk.Button(popup, text="Submit", command=lambda: on_submit())
        submit_button.pack(pady=10)

        popup.transient(self)
        popup.grab_set()
        self.wait_window(popup)

        return self.popup_value

    def print_quotes(self, quotes_list):
        """
        Print a list of quotes.
        
        Args:
            quotes_list (list): List of quotes to print.
        """
        self.clear_response()
        
        colour = 'blue'
        i = 1
        for quote in quotes_list:
            self.response_text.insert_text("\n--------- QUOTE " + str(i) + " ---------\n\n", 'bold', 'center')
            self.response_text.insert_text(quote['content'] + "\n", colour, 'center')
            self.response_text.insert_text("\n--------- AUTHOR ---------\n\n", 'bold', 'center')
            self.response_text.insert_text(quote['author_name'] + "\n", colour, 'center')
            self.response_text.insert_text("\n--------- TAGS ---------\n\n", 'bold', 'center')
            self.response_text.insert_text(quote['tags'] + "\n", colour, 'center')
            self.response_text.insert_text("\n========================================================================================" + "\n", 'bold', 'center')

            if colour == 'blue':
                colour = 'green'
            else:
                colour = 'blue'
            i += 1

        self.response_text.scroll_top()
        self.console_text.insert_text("All quotes printed." + "\n", "black") 

    def run_controller(self, query_case):
        """
        The Presenter/Controller function in the MVP/MVC pattern.
        
        Args:
            query_case (str): The query case to execute.
        """
        match query_case:

            case 'quotes_by_author':
                self.console_text.insert_text("Fetching the names of all the authors...\n", 'black')
                all_authors_names = self.model.run_model('metadata', 'all_authors')
                self.console_text.insert_text("Make your selection...\n", 'black')
                list_of_authors = all_authors_names[0]['key_value'].split(', ')

                selection = self.get_selection(list_of_authors)
                if selection:
                    author_name = selection[0]
                    self.console_text.insert_text("Your selection = " + author_name + "\n", 'black')
                    self.console_text.insert_text("Fetching 'quotes_by_author'...\n", 'black')
                    results = self.model.run_model('quotes_by_author', author_name)
                    self.print_quotes(results)
                else:
                    self.console_text.insert_text("Nothing was selected." + "\n", 'black')

            case 'x_quotes':
                self.console_text.insert_text("Retrieving your number...\n", 'black')
                
                x_quotes = self.get_input()
                if x_quotes:
                    self.console_text.insert_text("You typed in number: " + str(x_quotes) + "\n", 'black')
                    self.console_text.insert_text("Fetching 'x_quotes'...\n", 'black')
                    results = self.model.run_model('x_quotes', x_quotes)
                    self.print_quotes(results)
                else:
                    self.console_text.insert_text("No valid input was entered.\n", 'black')

            case 'random_quote':
                self.console_text.insert_text("Fetching 'random_quote'...\n", 'black')
                results = self.model.run_model('random_quote')
                self.print_quotes(results)

            case 'total_quotes':
                self.console_text.insert_text("Fetching 'total_quotes'...\n", 'black')
                results = self.model.run_model('total_quotes')
                
                self.clear_response()
                self.response_text.insert_text("\n--------- TOTAL QUOTES ---------\n", 'bold', 'center')
                self.response_text.insert_text("\nThere are a total of ", 'blue', 'center')
                self.response_text.insert_text(str(results[0]['total_quotes']) + " quotes in the Happy Quotes database.\n", 'blue', 'center')
                self.response_text.insert_text("\nSome people say that you just can't have enough quotes...", 'blue', 'center')

                self.console_text.insert_text("Printed 'total_quotes'.\n", 'black')

            case 'quotes_by_tag':
                self.console_text.insert_text("Fetching the list of all the tags...\n", 'black')
                all_tags = self.model.run_model('metadata', 'all_tags')
                self.console_text.insert_text("Make your selection...\n", 'black')
                list_of_tags = all_tags[0]['key_value'].split(', ')

                selection = self.get_selection(list_of_tags)
                if selection:
                    tag = selection[0]
                    self.console_text.insert_text("Your selection = " + tag + "\n", 'black')
                    self.console_text.insert_text("Fetching 'quotes_by_tag'...\n", 'black')
                    results = self.model.run_model('quotes_by_tag', tag)
                    self.print_quotes(results)
                else:
                    self.console_text.insert_text("Nothing was selected." + "\n", 'black')

            case 'top5_authors':
                self.console_text.insert_text("Fetching 'top5_authors'...\n", 'black')
                results = self.model.run_model('top5_authors')

                self.clear_response()
                self.response_text.insert_text("\n--------- TOP 5 AUTHORS ---------\n\n", 'bold', 'center')
                
                colour = 'blue'
                i = 1
                for result in results:
                    self.response_text.insert_text("\n" + str(i) + "- " + result['name'] + " , ", colour, 'center')
                    self.response_text.insert_text("total quotes = " + str(result['quote_count']) + "\n", colour, 'center')
                    i += 1
                    colour = ('green' if colour == 'blue' else 'blue')

                self.console_text.insert_text("Printed 'top5_authors'.\n", 'black')

            case 'comments_random_quote':
                self.console_text.insert_text("Fetching 'comments_random_quote'...\n", 'black')
                comments, quote = self.model.run_model('comments_random_quote')
                
                self.clear_response()

                self.response_text.insert_text("\n--------- RANDOM QUOTE ---------\n\n", 'bold', 'center')
                self.response_text.insert_text(quote[0]['content'] + "\n\n", 'blue', 'center')
                self.response_text.insert_text("\n--------- ALL COMMENTS: ---------\n\n", 'bold', 'center')

                colour = 'blue'
                i = 1
                for comment in comments:
                    self.response_text.insert_text("\n--------- COMMENT: " + str(i) + " ---------\n", 'bold', 'center')
                    self.response_text.insert_text(comment['title'] + "\n", colour, 'center')
                    self.response_text.insert_text("\n--------- DETAILS ---------\n", 'bold', 'center')
                    self.response_text.insert_text(comment['details'] + "\n", colour, 'center')
                    self.response_text.insert_text("\n--------- USER EMAIL ---------\n", 'bold', 'center')
                    self.response_text.insert_text(comment['user_email'] + "\n", colour, 'center')
                    self.response_text.insert_text("\n========================================================================================" + "\n", 'bold', 'center')

                    i += 1
                    colour = ('green' if colour == 'blue' else 'blue')

                self.response_text.scroll_top()
                self.console_text.insert_text("Printed the details for the quote's comments." + "\n", "black")
            
            case 'author_bio':
                self.console_text.insert_text("Fetching the names of all the authors...\n", 'black')
                all_authors_names = self.model.run_model('metadata', 'all_authors')
                self.console_text.insert_text("Make your selection...\n", 'black')
                list_of_authors = all_authors_names[0]['key_value'].split(', ')
                
                selection = self.get_selection(list_of_authors)
                if selection:
                    author_name = selection[0]
                    self.console_text.insert_text("Your selection = " + author_name + "\n", 'black')
                    self.console_text.insert_text("Fetching 'author_bio'...\n", 'black')
                    results = self.model.run_model('author_bio', author_name)

                    self.clear_response()
                    
                    colour = 'blue'
                    for result in results:
                        self.response_text.insert_text("\n--------- NAME ---------\n\n", 'bold', 'center')
                        self.response_text.insert_text(result['name'] + "\n", colour, 'center')
                        self.response_text.insert_text("\n--------- BIRTH DATE ---------\n\n", 'bold', 'center')
                        self.response_text.insert_text(str(result['birth_date']) + "\n", colour, 'center')
                        self.response_text.insert_text("\n--------- BIO ---------\n\n", 'bold', 'center')
                        self.response_text.insert_text(result['description'] + "\n", colour, 'center')

                    self.response_text.scroll_top()
                    self.console_text.insert_text("Printed the author's biography." + "\n", "black")
                else:
                    self.console_text.insert_text("Nothing was selected." + "\n", 'black')

            case 'all_quotes':
                self.console_text.insert_text("Fetching 'all_quotes'." + "\n", "black")
                results = self.model.run_model('all_quotes')
                self.print_quotes(results)
            
            case 'surprise':
                all_tags = self.model.run_model('metadata', 'all_tags')
                list_of_tags = all_tags[0]['key_value'].split(', ')

                all_authors_names = self.model.run_model('metadata', 'all_authors')
                list_of_authors = all_authors_names[0]['key_value'].split(', ')

                my_options = ['authors', 'tags']  
                surprise = random.choice(my_options)
                self.console_text.insert_text("Fetching your surprise...\n", 'black')
                
                if surprise == 'authors':
                    author_name = random.choice(list_of_authors)
                    self.console_text.insert_text("Fetching surprise author: " + author_name + "...\n", 'black')
                    results = self.model.run_model('quotes_by_author', author_name)
                    self.print_quotes(results)

                else:
                    tag = random.choice(list_of_tags)
                    self.console_text.insert_text("Fetching surprise tag: " + tag + "...\n", 'black')
                    results = self.model.run_model('quotes_by_tag', tag)
                    self.print_quotes(results)                    

            case 'qotd':
                self.console_text.insert_text("Fetching 'quote_of_the_day'...\n", 'black')
                results = self.model.run_model('random_quote')
                self.response_text.insert_text("\n\n\n--------- Quote Of The Day ---------\n\n\n", 'green', 'center')
                self.response_text.insert_text(results[0]['content'] + "\n\n", 'green', 'center')
                self.response_text.insert_text("by " + results[0]['author_name'] + "\n", 'green', 'center')
            
            case _:
                self.console_text.insert_text("Unknown query number!\n", 'red')
