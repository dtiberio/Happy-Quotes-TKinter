# Python
 
# this is the Main Loop

from happy_tk_gui import *
from happy_models import *
from dotenv import load_dotenv

#########
# INIT
#########

# Load the environment variables from the .env file
# 1. We get the Database name here, as MySQLDB() class allows one class instance for each database

load_dotenv('.env')
DB_NAME = os.getenv('DATABASE_NAME')

# 2. create the data Model, it includes all the methods to fetch the data
model = ModelQueries(DB_NAME)

# if DB_NAME exists, then MySQL returns a list with 1 dict, otherwise returns an empty list
sql_query = """
    SELECT SCHEMA_NAME 
    FROM INFORMATION_SCHEMA.SCHEMATA 
    WHERE SCHEMA_NAME = %s;
"""

# test if MySQL server is online
if model.db.test_connection():
    print("Database server is online.")
    # test if the database exists
    results = model.db.sql_query(sql_query, (DB_NAME,))
    if results:
        print(f"Successfully connected to database {DB_NAME}.")
    else:
        # if the database does not existe then terminate the program.
        print(f"Fatal Error! Database {DB_NAME} is missing. Terminating the program.")    
        sys.exit()
else:
    # if the database server is offline.
    print("Fatal Error! Database server is offline. Terminating the program.")    
    sys.exit()

#########
# MAIN LOOP
#########

# 3. Create the TKinter GUI, it includes the methods for the View and Controller
# The app gains access to the model created earlier, it has all the methods required to access the database
app = MyHappyGUI(model)

# 4. launch the GUI, this is the main window
app.mainloop()

#########
# EXIT
#########

# 5. This is executed after main window terminates
print("Thank you for using Happy Quotes! Goodbye!")

###
# this is the EOF