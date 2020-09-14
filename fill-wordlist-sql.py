import csv
import psycopg2
import psycopg2.extras

from time import time

# Path to csv file with wordlist.
words_file_path = "archive/words.csv"

# Read the file and put the words into a python list words_list.
with open(words_file_path, "r") as words_file:
    words_reader = csv.reader(words_file)
    print("Read words file.")
    print(words_reader)
    words_list = words_reader.__next__()
    print(len(words_list))
##    print(words_list)


# Joel enter the database url. No one else can know it (:
database_url = input("Enter the database URL:")

# Functions from app.py, could have put them in separate file and import or
# whatever but cba

# Function to connect to default main SQL database.
# Returns connection and cursor.
def postgresql_connect():
    conn = psycopg2.connect(database_url, sslmode='require')
    cur = conn.cursor()
    return conn, cur

# Function to close the connection to the database.
# Takes a connection and a cursor as arguments.
def postgresql_disconnect(conn, cur):
    cur.close()
    conn.close()

# Connect to database
conn, cur = postgresql_connect()


# Create list of tuples with arguments.
args_list = [(i, words_list[i]) for i in range(len(words_list))]
print("Prepared argument list.")
start_time = time()
# Run on SQL server.
psycopg2.extras.execute_batch(cur,
                              """
                              INSERT INTO wordlist(id, word, used)
                              VALUES (%s, %s, FALSE)
                              """,
                              args_list)

print("""
      Wrote {} columns to server in {} seconds, committing
      """.format(len(words_list, time()-start_time)))


# Commit and disconnect from server.
conn.commit()
postgresql_disconnect(conn, cur)