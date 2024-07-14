## Introduction

This Python tutorial is split across two main scripts.  

	1. An ETL script, implemented in a Jupyter Notebook.
	2. The user application, implemented in a TKinter GUI.

# Jupyter notebook ETL Script

This Jupyter notebook contains a Python script designed to perform ETL (Extract, Transform, Load) tasks for the HappyQuotes database. 

### 1. Data Extraction

It starts with the Data Extraction tasks:

	- It uses BeautifulSoup4 to extract quotes from the `quotes.toscrape.com` website.
	- It uses the requests library to call an API, `jsonplaceholder.typicode.com`, and retrive mock-up data to make up the comments for the quotes.

### 2. Data Transformation

The extracted data is transformed to fit the database schema. This involves:

	- Importing `happy_models.py` to levearege Pydantic to create four distinct types of objects  
	- Structuring quotes, authors, tags, and comments.
	- Cleaning malformed data to ensure consistency.
	- Extracting necessary metadata.

### 3. Data Loading

The transformed data is loaded into a MySQL database. This includes:  

	- Establishing a connection to the MySQL database.
	- Creating tables for quotes, authors, tags, comments, and metadata.
	- Inserting data into the respective tables.

## Happy Quotes Program

The Happy Quotes Program is a Python-based application that provides a graphical user interface (GUI) for interacting with the Happy Quotes database built by the ETL script.  
The application allows users to retrieve quotes by author, tag, or randomly, and also provides information about authors and their biographies.  
The program is built using the Tkinter library for the GUI and MySQL for the database.
To help structuring the code, the program follows the MVC application pattern.

## Features

	- Display quotes by specific authors
	- Retrieve a specified number of random quotes
	- Fetch a single random quote
	- Display the total number of quotes in the database
	- Select quotes by tag
	- Show the top 5 authors with the most quotes
	- Fetch all comments associated with a random quote
	- Display an author's biography
	- Retrieve all quotes in the database
	- Get a surprise selection of quotes based on random authors or tags

## How It Works

MVC/MVP Pattern
The Happy Quotes Program follows the Model-View-Controller (MVC) pattern, sometimes also referred to as the Model-View-Presenter (MVP) pattern in this context. This design pattern helps separate the concerns of the application, making it more modular, maintainable, and testable.

	- **Model**: Represents the data and the business logic of the application. In this program, ModelQueries acts as the Model, handling database interactions and data retrieval.  

	- **View**: Represents the user interface. In this program, MyHappyGUI acts as the View, managing the layout, widgets, and user interactions.

	- **Controller/Presenter**: Manages the communication between the Model and the View. It handles user input, processes it, and updates the View accordingly. In this program, the run_controller method in MyHappyGUI acts as the Controller/Presenter.

## How it is Implemented

1. `MyHappyGUI()` Class  

    The `MyHappyGUI()` class extends `tk.Tk` and represents the main window of the application. It is responsible for:

    - Creating the menu bar, main frames, and footer section
    - Defining widgets for displaying query responses and console messages
    - Handling user interactions and events
    - Running the main loop of the application
    - The `run_controller()` method in `MyHappyGUI()` acts as the Controller, coordinating between the user inputs from the View and the data processing by the Model.

2. `ModelQueries()` Class  

    The `ModelQueries()` class encapsulates all the SQL queries that the user can run.  
	It acts as the Model in the MVC/MVP pattern, managing the database interactions and data retrieval.

    - `run_model()`: This method takes a query_case identifier and an optional value, executes the corresponding query through a match-case statement and then returns the results to the Controller.

## Example of the MVC pattern

Here's a brief example of how the MVC/MVP pattern is implemented in this program:

    - User Interaction: The user selects `"Get X Random Quotes"` from the Queries menu.
    - View: `MyHappyGUI()` captures the user input from the menus and calls `run_controller()` with the query_case value of `'x_quotes'`.
    - Controller: the `run_controller()` processes additional user input by retrieving the number of quotes to fetch from the user, and calls `ModelQueries.run_model()` with the appropriate parameters.
    - Model: `ModelQueries.run_model()` executes the SQL query to fetch the random quotes from the database and then returns the results to the Controller.
    - View Update: `run_controller()` receives the results and updates the `response_text` widget in `MyHappyGUI()` to display the fetched quotes.

## Main files

	- `happyquotes_main.py` - the entry point to the program's main loop.  
	- `happy_models.py` - the required classes to handle the MySQL database connections, the data models and the Model class.  
	- `happy_tk_view.py` - the classes that implement the TKinter based View and the Controller.  
	- `happyquotes-ETL-script.ipynb` - the Jupyter Notebook that implements the ETL script.  
	- `TUTORIAL.TXT` - The user guide, explaining how to interact with the TKinter GUI.  
	- `.\img\` - the subfolder storing a few screenshots with details about the variables, classes e database tables.  
	- `.env` - the file storing the database settings, make sure it's updated with the settings for your environment.  
	- `requirements.txts` - the list of python libraries required to run this program.  

## Requirements

	- Python 3.11+
	- Tkinter
	- Pydantic
	- Pydantic [email]
	- MySQL Connector/Python
	- Python-dotenv
	- BeautifulSoup 4
	- Requests

## Installation

1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Set up your MySQL database and update the `.env` file with your database credentials.

## Usage

To run the application, simply execute the main script:
	```bash
	python happyquotes_main.py
	```