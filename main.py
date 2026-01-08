#
# header comment!
#
import sqlite3
import objecttier

#Prints general statistics about the database.
def one(dbConn):
    #Does the functions for the relevant portions of this user request:
    numMovies = objecttier.num_movies(dbConn)
    numReviews = objecttier.num_reviews(dbConn)
    print("General Statistics:")
    print(f"  Number of Movies: {numMovies:,}")
    print(f"  Number of Reviews: {numReviews:,}")

#Find movies matching a pattern.
def two(dbConn):
    movieSearch = input("Enter the name of the movie to find (wildcards _ and % allowed): ")
    print()
    movieList = objecttier.get_movies(dbConn, movieSearch)
    listLength = len(movieList)
    print(f"Number of Movies Found: {listLength}")
    if listLength == 0:
        return
    print()
    if listLength > 100:
        print("There are too many movies to display (more than 100). Please narrow your search and try again.")
        return
    for movie in movieList:
        print(f"{movie.Movie_ID} : {movie.Title} ({movie.Release_Year})")

#Find movie details.
def three(dbConn):
    movie_id = input("Enter a movie ID: ")
    print()
    movieObject = objecttier.get_movie_details(dbConn, movie_id)
    if movieObject is None:
        print("No movie matching that ID was found in the database.")
        return
    else:
        print(f"{movie_id} : {movieObject.Title}")
        print(f"  Release date: {movieObject.Release_Date}")
        print(f"  Runtime: {movieObject.Runtime} (minutes)")
        print(f"  Original language: {movieObject.Original_Language}")
        print(f"  Budget: ${movieObject.Budget:,} (USD)")
        print(f"  Revenue: ${movieObject.Revenue:,} (USD)")
        print(f"  Number of reviews: {movieObject.Num_Reviews}")
        print(f"  Average rating: {movieObject.Avg_Rating:.2f} (0-10)")
        print(f"  Genres: ", end = "")
        for i, Genre in enumerate(movieObject.Genres):
                print(f"{Genre}, ", end = "")
        print()
        print(f"  Production companies: ", end = "")
        for i, Production_Company in enumerate(movieObject.Production_Companies):
                print(f"{Production_Company}, ", end = "")
        print()
        print(f"  Tagline: {movieObject.Tagline}")

#Shows the top N movies with a minimum number of ratings.
def four(dbConn):
    N = int(input("Enter a value for N: "))
    if N < 1:
        print("Please enter a positive value for N.")
        return
    min_num_reviews = int(input("Enter a value for the minimum number of reviews: "))
    if min_num_reviews < 1:
        print("Please enter a positive value for the minimum number of reviews.")
        return
    print()
    movieRatingsList =  objecttier.get_top_N_movies(dbConn, N, min_num_reviews)
    if len(movieRatingsList) == 0:
        print("No movies were found that fit the criteria.")
    for movieRating in movieRatingsList:
        print(f"{movieRating.Movie_ID} : {movieRating.Title} ({movieRating.Release_Year}), Average rating = {movieRating.Avg_Rating:.2f} ({movieRating.Num_Reviews} reviews)")

#Adds a new review for a movie.
def five(dbConn):
    rating = int(input("Enter a value for the new rating (0-10): "))
    if rating < 0 or rating > 10:
        print("Invalid rating. Please enter a value between 0 and 10 (inclusive).")
        return
    movie_id = input("Enter a movie ID: ")
    print()

    returnStatus = objecttier.add_review(dbConn, movie_id, rating)
    if returnStatus == 0:
        print("No movie matching that ID was found in the database.")
    else:
        print("Rating was successfully inserted into the database.")

#Sets the tagline of a movie.
def six(dbConn):
    tagline = input("Enter a tagline: ")
    movie_id = input("Enter a movie ID: ")
    print()
    returnStatus = objecttier.set_tagline(dbConn, movie_id, tagline)
    if returnStatus == 0:
        print("No movie matching that ID was found in the database.")
    else:
        print("Tagline was successfully set in the database.")

def errormsg():
    print("Error, unknown command, try again...")

##################################################################  
#
# main
#
print("Project 2: Movie Database App (N-Tier)")
print("CS 341, Spring 2025")
print()
print("This application allows you to analyze various")
print("aspects of the MovieLens database.")
print()

#Adds database connection that is passed to each function call depending on the user's choice.
dbName = input("Enter the name of the database you would like to use: ")
dbConn = sqlite3.connect(dbName)

print()
print("Successfully connected to the database!")

exitState = 0
#exitState enables this portion of the main function to be on a loop until the user specifies to exit with the 'x' symbol.
while exitState == 0:
    print()
    print("Select a menu option: ")
    print("  1. Print general statistics about the database")
    print("  2. Find movies matching a pattern for the name")
    print("  3. Find details of a movie by movie ID")
    print("  4. Top N movies by average rating, with a minimum number of reviews")
    print("  5. Add a new review for a movie")
    print("  6. Set the tagline of a movie")
    print("or x to exit the program.")
    cmd = input("Your choice --> ")
    print()
    if cmd == "1":
        one(dbConn)
    elif cmd == "2":
        two(dbConn)
    elif cmd == "3":
        three(dbConn)
    elif cmd == "4":
        four(dbConn)
    elif cmd == "5":
        five(dbConn)
    elif cmd == "6":
        six(dbConn)
    elif cmd == "x":
        exitState = 1
    else:
        errormsg()




print("Exiting program.")