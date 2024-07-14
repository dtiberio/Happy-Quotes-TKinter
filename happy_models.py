# Python

from pydantic import BaseModel, EmailStr, Field, PositiveInt
from typing import List, Optional
from datetime import date
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# MySQLDB() manages the connection to the database server
class MySQLDB:
    # this class handles the connection to the DB server, the connection details must be stored in the .env file
    # the database name must be set at object instatiation
    # it's possible to work with several databases hosted on the same server by instantiating an object for each database
    
    def __init__(self, database: str, env_file='.env'):
        """
        Initialize the MySQLDB instance with the specified database and environment file.
        
        Args:
            database (str): Name of the database to connect to.
            env_file (str): Path to the environment file containing DB credentials.
        """
        # Load the environment variables from the .env file
        load_dotenv(env_file)
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.port = os.getenv('DB_PORT')
        self.database = database

    def test_connection(self):
        """
        Test the connection to the database server.
        
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        # Establish the connection to the server, doesn't connect to any database
        conn = None
        try:
            conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )

            if conn.is_connected():
                print("Connection to the DB server was successful.")
                return True
            else:
                print("Failed to connect to the DB server.")
                return False

        except Error as e:
            print(f"Error: {e}")
            return False

        finally:
            if conn and conn.is_connected():
                conn.close()
                print("DB server connection closed.")

    def sql_execute(self, sql: str, val=()):
        """
        Execute a SQL command (INSERT, UPDATE, DELETE).
        
        Args:
            sql (str): SQL query to execute.
            val (tuple): Values to use in the SQL query.
            
        Returns:
            tuple: Number of affected rows and last inserted row ID.
        """
        # execute a 'sql' command, use variables from the 'val' tuple
        # use for executing statements like INSERT, UPDATE, or DELETE
        # returns the number of affected rows and the last inserted row ID

        conn = None
        cursor = None
        try:
            # Establish the connection
            conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            cursor = conn.cursor()
            cursor.execute(sql, val)
            conn.commit()
            rowcount = cursor.rowcount
            lastrowid = cursor.lastrowid
            return rowcount, lastrowid

        except Error as e:
            print(f"Error: {e}")
            return None, None

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                print("Database connection closed.")

    def sql_query(self, sql: str, val=()):
        """
        Execute a SELECT query and return the results.
        
        Args:
            sql (str): SQL query to execute.
            val (tuple): Values to use in the SQL query.
            
        Returns:
            list: Fetched results as a list of dictionaries.
        """
        # for executing SELECT queries and returning results
        # returns the fetched results as a list of dictionaries
        conn = None
        cursor = None
        try:
            # Establish the connection to the specified database
            conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            # creates a cursor that returns results as dictionaries instead of tuples. 
            # allows access to columns by their names instead of their positional indexes.
            cursor = conn.cursor(dictionary=True)

            # Execute the SELECT query with the provided condition
            cursor.execute(sql, val)
            results = cursor.fetchall()
            return results

        except Error as e:
            print(f"Error: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                print("Database connection closed.")

    def create_database(self, overwrite: bool = False):
        """
        Create a new database or check if it exists.
        
        Args:
            overwrite (bool): If True, overwrite an existing database.
            
        Returns:
            bool: True if database is created or exists, False otherwise.
        """
        # this method can create or test if a database exists
        # create_database(False) --> do not overwrite an existing database
        # create_database(True) --> overwrite an existing database
        conn = None
        cursor = None
        try:
            # Establish the connection
            conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                autocommit=True
            )
            cursor = conn.cursor()

            # Check if the database exists
            cursor.execute(f"SHOW DATABASES LIKE '{self.database}'")
            result = cursor.fetchone()

            if result:
                if overwrite:
                    # Drop the existing database
                    cursor.execute(f"DROP DATABASE {self.database}")
                    print(f"Database {self.database} dropped.")
                else:
                    print(f"Database {self.database} already exists.")
                    return True

            # Create the new database
            cursor.execute(f"CREATE DATABASE {self.database}")
            print(f"Database {self.database} created.")
            return True

        except Error as e:
            print(f"Error: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                print("Database connection closed.")

    def create_table(self, table_name: str, sql_code: str, overwrite: bool = False):
        """
        Create a new table in the database or check if it exists.
        
        Args:
            table_name (str): Name of the table to create.
            sql_code (str): SQL code to create the table.
            overwrite (bool): If True, overwrite an existing table.
            
        Returns:
            bool: True if table is created or exists, False otherwise.
        """
        # checks if a table exists before executing the 'sql' code to create it
        # if overwrite == True, then overwrite an existing table
        conn = None
        cursor = None
        try:
            # Establish the connection to the specified database
            conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            cursor = conn.cursor()

            # Check if the table exists
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cursor.fetchone()

            if result:
                if overwrite:
                    # Drop the existing table
                    cursor.execute(f"DROP TABLE {table_name}")
                    print(f"Table {table_name} dropped.")
                else:
                    print(f"Table {table_name} already exists in database {self.database}.")
                    return

            # Create the new table
            cursor.execute(sql_code)
            print(f"Table {table_name} created in database {self.database}.")
            return True

        except Error as e:
            print(f"Error: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                print("Database connection closed.")

# All the following classes are Pydantic V2 classes.
# They leverage Pydantic's type annotations and validations,
# this way, we avoid writing getters and setters for each attribute,
# and we get Pydantic to check the data types automatically.

class Quote(BaseModel):
    id_quote: Optional[PositiveInt] = Field(None, alias='id_quote')
    content: str = Field(..., alias='content')
    author_id: Optional[PositiveInt] = Field(None, alias='author_id')
    tags: List[str] = Field(..., alias='tags')

    def db_save(self, db: MySQLDB):
        """
        Save the quote to the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            
        Returns:
            tuple: Number of affected rows and last inserted row ID.
        """
        sql = """
        INSERT INTO quote (content, author_id, tags)
        VALUES (%s, %s, %s)
        """
        
        # the list 'tags' is transformed into a string before inserting into the database
        val = (self.content, self.author_id, ', '.join(self.tags))
        rowcount, lastrowid = db.sql_execute(sql, val)
        if lastrowid:
            self.id_quote = lastrowid   # assign id to object
        return rowcount, lastrowid

    def fetch_all(db: MySQLDB):
        """
        Fetch all quotes from the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            
        Returns:
            list: List of dictionaries containing all quotes.
        """
        sql_query = """
        SELECT 
        q.content AS content,
        a.name AS author_name,
        q.tags AS tags
        FROM quote q
        JOIN author a ON q.author_id = a.id_author
        """
        results = db.sql_query(sql_query, ())
        return results   # returns a list of dicts, else the db returns []
    
    def fetch_by_id(db: MySQLDB, quote_id: int):
        """
        Fetch a quote by its ID from the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            quote_id (int): ID of the quote to fetch.
            
        Returns:
            list: List containing one dictionary with quote details, or an empty list if not found.
        """
        sql_query = """
        SELECT 
        q.content AS content,
        a.name AS author_name,
        q.tags AS tags
        FROM quote q
        JOIN author a ON q.author_id = a.id_author
        WHERE q.id_quote = %s
        """
        val = (quote_id,)
        result = db.sql_query(sql_query, val)
        return result      # if quote_id exists, then returns list with one dict, else the db returns []

    
    def fetch_by_tag(db: MySQLDB, tag: str):
        """
        Fetch quotes by tag from the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            tag (str): Tag to filter quotes.
            
        Returns:
            list: List of dictionaries containing quotes with the specified tag.
        """
        sql_query = """
        SELECT 
        q.content AS content,
        a.name AS author_name,
        q.tags AS tags
        FROM quote q
        JOIN author a ON q.author_id = a.id_author
        WHERE q.tags LIKE %s
        """
        val = ("%" + tag + "%",)
        result = db.sql_query(sql_query, val)
        return result      # if tag exists, then returns list of dicts, else the db returns []


    def fetch_by_author(db: MySQLDB, author_name: str):
        """
        Fetch quotes by author from the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            author_name (str): Author name to filter quotes.
            
        Returns:
            list: List of dictionaries containing quotes by the specified author.
        """
        sql_query = """
        SELECT 
        q.content AS content,
        a.name AS author_name,
        q.tags AS tags
        FROM quote q
        JOIN author a ON q.author_id = a.id_author
        WHERE a.name LIKE %s
        """
        val = (author_name,)
        results = db.sql_query(sql_query, val)
        return results      # if author_name exists, then returns list of dicts, else the db returns []

class Author(BaseModel):
    id_author: Optional[PositiveInt] = Field(None, alias='id_author')
    name: str = Field(..., alias='name')
    birth_date: date = Field(..., alias='birth_date')
    birth_city: Optional[str] = Field(..., alias='birth_city')
    birth_state: Optional[str] = Field(..., alias='birth_state')
    birth_country: Optional[str] = Field(..., alias='birth_country')
    description: str = Field(..., alias='description')

    def db_save(self, db: MySQLDB):
        """
        Save the author to the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            
        Returns:
            tuple: Number of affected rows and last inserted row ID.
        """
        sql = """
        INSERT INTO author (name, birth_date, birth_city, birth_state, birth_country, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (self.name, self.birth_date, self.birth_city, self.birth_state, self.birth_country, self.description)
        rowcount, lastrowid = db.sql_execute(sql, val)
        if lastrowid:
            self.id_author = lastrowid  # assign id to object
        return rowcount, lastrowid
    
    def fetch_all(db: MySQLDB):
        """
        Fetch all authors from the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            
        Returns:
            list: List of dictionaries containing all authors.
        """
        sql_query = """
        SELECT name, birth_date, birth_city, birth_state, birth_country, description
        FROM author
        """
        results = db.sql_query(sql_query, ())
        return results   # returns a list of dicts, else the db returns []
    
    def fetch_by_id(db: MySQLDB, author_id: int):
        """
        Fetch an author by their ID from the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            author_id (int): ID of the author to fetch.
            
        Returns:
            list: List containing one dictionary with author details, or an empty list if not found.
        """
        sql_query = """
        SELECT name, birth_date, birth_city, birth_state, birth_country, description
        FROM author
        WHERE id_author = %s""" 
        val = (author_id,)
        result = db.sql_query(sql_query, val)
        return result      # if author_id exists, then returns list with one dict, else the db returns []

    
    def fetch_by_name(db: MySQLDB, author_name: str):
        """
        Fetch an author by their name from the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            author_name (str): Name of the author to fetch.
            
        Returns:
            list: List containing one dictionary with author details, or an empty list if not found.
        """
        sql_query = """
        SELECT name, birth_date, birth_city, birth_state, birth_country, description
        FROM author
        WHERE name LIKE %s""" 
        val = (author_name,)
        result = db.sql_query(sql_query, val)
        return result      # if author_name exists, then returns list with one dict, else the db returns []

class Comment(BaseModel):
    id_comment: Optional[PositiveInt] = Field(None, alias='id_comment')
    quote_id: PositiveInt = Field(..., alias='quote_id')
    title: str = Field(..., alias='title')
    details: str = Field(..., alias='details')
    user_email: EmailStr = Field(..., alias='user_email')

    def db_save(self, db: MySQLDB):
        """
        Save the comment to the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            
        Returns:
            tuple: Number of affected rows and last inserted row ID.
        """
        sql = """
        INSERT INTO comment (quote_id, title, details, user_email)
        VALUES (%s, %s, %s, %s)
        """
        val = (self.quote_id, self.title, self.details, self.user_email)
        rowcount, lastrowid = db.sql_execute(sql, val)
        if lastrowid:
            self.id_comment = lastrowid     # assign id to object
        return rowcount, lastrowid
    
    def fetch_by_quote_id(db: MySQLDB, quote_id: int):
        """
        Fetch comments by quote ID from the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            quote_id (int): ID of the quote to filter comments.
            
        Returns:
            list: List of dictionaries containing comments for the specified quote.
        """
        sql_query = """
        SELECT title, details, user_email
        FROM comment
        WHERE quote_id = %s""" 
        val = (quote_id,)
        result = db.sql_query(sql_query, val)
        return result      # if quote_id exists, then returns list of dicts, else the db returns []

class Metadata(BaseModel):
    id_key: Optional[PositiveInt] = Field(None, alias='id_key')
    key_name: str = Field(..., alias='key_name')
    key_value: List[str] = Field(..., alias='key_value')

    def db_save(self, db: MySQLDB):
        """
        Save the metadata to the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            
        Returns:
            tuple: Number of affected rows and last inserted row ID.
        """
        sql = """
        INSERT INTO metadata (key_name, key_value)
        VALUES (%s, %s)
        """

        # transform the list of key_values into a string before inserting into the database
        val = (self.key_name, ', '.join(self.key_value))
        rowcount, lastrowid = db.sql_execute(sql, val)
        if lastrowid:
            self.id_key = lastrowid     # assign id to object
        return rowcount, lastrowid
    
    def fetch_by_key_name(db: MySQLDB, key_name: str):
        """
        Fetch metadata by key name from the database.
        
        Args:
            db (MySQLDB): Database connection instance.
            key_name (str): Key name to filter metadata.
            
        Returns:
            list: List containing one dictionary with metadata details, or an empty list if not found.
        """
        sql_query = """
        SELECT key_value
        FROM metadata
        WHERE key_name = %s""" 
        val = (key_name,)
        result = db.sql_query(sql_query, val)
        return result      # returns list with one dict, else the db returns []

# the ModelQueries() class encapsulates all the SQL queries that will be run by the user
# this class is meant to be the Model that is used by the TKinter View-Controller
# it provides an API to retrieve data from the database, 
# without the TKinter View-Controller having to know the details of the tables

class ModelQueries:
    def __init__(self, database: str):
        """
        Initialize the ModelQueries instance with the specified database.
        This class implements the Model in the MVP/MVC pattern.
        
        Args:
            database (str): Name of the database to connect to.
        """
        self.db = MySQLDB(database)

    def run_model(self, query_case, value=None):
        """
        Run the specified query based on the query case.
        
        Args:
            query_case (str): The case specifying which query to run.
            value (str, optional): The value to use in the query.
            
        Returns:
            list or tuple: Results of the query.
        """
        # These are all the queries available to run in the GUI
        match query_case:
            case ('quotes_by_author'):
                return Quote.fetch_by_author(self.db, value) # list of dicts
            
            case ('x_quotes'):
                # return a list of 'value' random quotes
                results = self.db.sql_query("""
                SELECT 
                    q.content,
                    a.name AS author_name,
                    q.tags
                FROM 
                    quote q
                JOIN 
                    author a ON q.author_id = a.id_author
                ORDER BY 
                    RAND()
                LIMIT 
                    %s
                """, (value,))
                                
                return results    # list of dicts
            
            case ('random_quote'):
                # return one random quote
                results = self.db.sql_query("""
                SELECT 
                    q.content,
                    a.name AS author_name,
                    q.tags
                FROM 
                    quote q
                JOIN 
                    author a ON q.author_id = a.id_author
                ORDER BY 
                    RAND()
                LIMIT 
                    1
                """, ())
                                
                return results    # list of dicts
            
            case ('total_quotes'):
                # return count of total quotes
                results = self.db.sql_query("""
                SELECT 
                    COUNT(*) AS total_quotes
                FROM 
                    quote;
                """, ())
  
                return results    # list of dicts
            
            case ('quotes_by_tag'):
                return Quote.fetch_by_tag(self.db, value) # list of dicts
            
            case ('top5_authors'):
                # return TOP 5 Authors by total quotes
                results = self.db.sql_query("""
                SELECT 
                    a.name,
                    COUNT(q.id_quote) AS quote_count
                FROM 
                    author a
                JOIN 
                    quote q ON a.id_author = q.author_id
                GROUP BY 
                    a.name
                ORDER BY 
                    quote_count DESC
                LIMIT 
                    5;
                """, ())
  
                return results    # list of dicts
            
            case ('comments_random_quote'):
                # note: works better if queries are split in 2
                # return id for one random quote
                rand_id = self.db.sql_query("""
                    SELECT 
                        id_quote
                    FROM 
                        quote
                    ORDER BY 
                        RAND()
                    LIMIT 1
                """, ())

                # return the random quote
                value = rand_id[0]['id_quote']
                random_quote = Quote.fetch_by_id(self.db, value)
                
                # return all comments from one random quote
                results = self.db.sql_query("""
                SELECT 
                    title,
                    details,
                    user_email
                FROM 
                    comment
                WHERE 
                    quote_id = %s;
                """, (value, ))

                return results, random_quote    # 2 x list of dicts
            
            case ('author_bio'):
                return Author.fetch_by_name(self.db, value) # list of dicts
            
            case ('all_quotes'):
                return Quote.fetch_all(self.db) # list of dicts
            
            case ('metadata'):
                return Metadata.fetch_by_key_name(self.db, value)

            case _:
                return []