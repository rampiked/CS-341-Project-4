Matt Sagat
University of Illinois Chicago 
CS 341 Project 4

This is a multi-tiered command-line based application that allows users to upload a Movie database (stored on my local machine due to Github file size constraints), 
then search or modify the database by converting user menu selections and string inputs into SQL queries.

These are the command line menu options:
"Select a menu option: 
  1. Print general statistics about the database
  2. Find movies matching a pattern for the name
  3. Find details of a movie by movie ID
  4. Top N movies by average rating, with a minimum number of reviews
  5. Add a new review for a movie
  6. Set the tagline of a movie
or x to exit the program."

Brief overview:
main.py takes user input (for what they want to do with the database) and passes it to the relevant function in objecttier.py. objecttier.py will create a SQL query,
then datatier.py will execute the SQL query. In the end, objecttier.py will return the appropriate values to main, and main will print them to the user.

Database heuristics:
Each movie database contains seven tables, which all have unique column names. If you are curious about particular fields, or the actual SQL queries, look at the functions in objecttier.py.
