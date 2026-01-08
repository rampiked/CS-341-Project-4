#
# objecttier.py
# Builds Movie-related objects from data retrieved through 
# the data tier.
import datatier

##################################################################
#
# Movie class:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
   def __init__(self, Movie_ID, Title, Release_Year):
      self.Movie_ID = Movie_ID
      self.Title = Title
      self.Release_Year = Release_Year

##################################################################
#
# MovieRating class:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating(Movie):
   def __init__(self, Movie_ID, Title, Release_Year, Num_Reviews, Avg_Rating):
      Movie.__init__(self, Movie_ID, Title, Release_Year)
      self.Num_Reviews = Num_Reviews
      self.Avg_Rating = Avg_Rating

##################################################################
#
# MovieDetails class:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list
#   Production_Companies: list
#
class MovieDetails:
   def __init__(self, Movie_ID, Title, Release_Date, Runtime, Original_Language, Budget, Revenue, Num_Reviews, Avg_Rating, Tagline, Genres, Production_Companies):
      self.Movie_ID = Movie_ID
      self.Title = Title
      self.Release_Date = Release_Date
      self.Runtime = Runtime
      self.Original_Language = Original_Language
      self.Budget = Budget
      self.Revenue = Revenue
      self.Num_Reviews = Num_Reviews
      self.Avg_Rating = Avg_Rating
      self.Tagline = Tagline
      self.Genres = Genres
      self.Production_Companies = Production_Companies

##################################################################
# 
# num_movies:
#
# Returns: the number of movies in the database, or
#          -1 if an error occurs
# 
def num_movies(dbConn):
   sql = """SELECT Count(Movies.Movie_ID) FROM Movies;"""
   result = datatier.select_one_row(dbConn, sql, [])
   return result[0]
   #Create SQL query and pass into one of the datatier commands.

##################################################################
# 
# num_reviews:
#
# Returns: the number of reviews in the database, or
#          -1 if an error occurs
#
def num_reviews(dbConn):
   sql = """SELECT Count(Ratings.Rating) FROM Ratings;"""
   result = datatier.select_one_row(dbConn, sql, [])
   return result[0]

##################################################################
#
# get_movies:
#
# Finds and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all movies.
#
# Returns: list of movies in ascending order by name, or
#          an empty list, which means that the query did 
#          not retrieve any data
#          (or an internal error occurred, in which case 
#          an error message is already output).
#
def get_movies(dbConn, pattern):
   sql = """SELECT Movies.Movie_ID, Movies.Title, strftime('%Y', Movies.Release_Date) FROM Movies WHERE Movies.Title LIKE ? ORDER BY Movies.Movie_ID ASC;"""
   result = datatier.select_n_rows(dbConn, sql, [pattern])

   movies = []
   for row in result:
      movies.append(Movie(row[0], row[1], row[2]))

   return movies

##################################################################
#
# get_movie_details:
#
# Finds and returns details about the given movie.
# The movie ID is passed as a parameter (originally from the user)
# and the function returns a MovieDetails object.
# If no movie was found matching that ID, the function returns
# None.
#
# Returns: a MovieDetails object if the search was successful, or
#          None if the search did not find a matching movie
#          (or an internal error occurred, in which case 
#          an error message is already output).
#
def get_movie_details(dbConn, movie_id):
   #Do multiple queries to make information easier to obtain, 
   sql = """SELECT Movies.Movie_ID, Movies.Title, DATE(Movies.Release_Date) AS Release_Date, Movies.Runtime, Movies.Original_Language, Movies.Budget, Movies.Revenue, 
   (SELECT COUNT(Ratings.Rating) FROM Ratings WHERE Ratings.Movie_ID = Movies.Movie_ID) AS Num_Reviews, AVG(Ratings.Rating) AS Avg_Rating,
   Movie_Taglines.Tagline,
   GROUP_CONCAT(DISTINCT Genres.Genre_Name) AS Genres, GROUP_CONCAT(DISTINCT Companies.Company_Name) AS Production_Companies
   FROM Movies
   LEFT JOIN Ratings ON Movies.Movie_ID = Ratings.Movie_ID
   LEFT JOIN Movie_Taglines ON Movies.Movie_ID = Movie_Taglines.Movie_ID
   LEFT JOIN Movie_Genres ON Movies.Movie_ID = Movie_Genres.Movie_ID
   LEFT JOIN Genres ON Movie_Genres.Genre_ID = Genres.Genre_ID
   LEFT JOIN Movie_Production_Companies ON Movies.Movie_ID = Movie_Production_Companies.Movie_ID
   LEFT JOIN Companies ON Movie_Production_Companies.Company_ID = Companies.Company_ID
   WHERE Movies.Movie_ID = ?
   GROUP BY Movies.Movie_ID;"""
   result = datatier.select_n_rows(dbConn, sql, [movie_id])

   if result:
      movie_info = result[0]

      movie_details = MovieDetails(
         Movie_ID = movie_info[0],
         Title = movie_info[1],
         Release_Date = movie_info[2],
         Runtime = movie_info[3],
         Original_Language = movie_info[4],
         Budget = movie_info[5],
         Revenue = movie_info[6],
         Num_Reviews = movie_info[7],
         Avg_Rating = movie_info[8] if movie_info[8] is not None else 0,
         Tagline = movie_info[9] if movie_info[9] is not None else "",
         Genres = sorted(movie_info[10].split(',')) if movie_info[10] else [],
         Production_Companies = sorted(movie_info[11].split(',')) if movie_info[11] else []
       )
      return movie_details
   else:
      return None
         

##################################################################
#
# get_top_N_movies:
#
# Finds and returns the top N movies based on their average 
# rating, where each movie has at least the specified number of
# reviews.
# Example: get_top_N_movies(10, 100) will return the top 10 movies
#          with at least 100 reviews.
#
# Returns: a list of 0 or more MovieRating objects
#          note that if the list is empty, it may be because the 
#          minimum number of reviews was too high
#          (or an internal error occurred, in which case 
#          an error message is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
   sql = """SELECT Movies.Movie_ID, Movies.Title, strftime('%Y', Movies.Release_Date) as Release_Year, Count(Ratings.Rating) as ratings,
   Avg(Ratings.Rating) as Avg_Ratings FROM Movies JOIN Ratings on Movies.Movie_ID = Ratings.Movie_ID GROUP BY Movies.Movie_ID 
   HAVING Count(Ratings.Rating) >= ?
   ORDER BY Avg_Ratings DESC
   LIMIT ?;"""
   result = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])

   movies = []
   for row in result:
      movies.append(MovieRating(row[0], row[1], row[2], row[3], row[4]))

   return movies


##################################################################
#
# add_review:
#
# Inserts the given review (a rating value between 0 and 10) into
# the database for the given movie.
# It is considered an error if the movie does not exist, and 
# the review is not inserted.
#
# Returns: 1 if the review was successfully added, or
#          0 if not (e.g. if the movie does not exist, or
#                    if an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
   check_movie_sql = "SELECT 1 FROM movies WHERE movie_id = ?"
   movie_row = datatier.select_one_row(dbConn, check_movie_sql, [movie_id])

   if movie_row == () or movie_row is None:
      return 0
   
   sql = "INSERT INTO Ratings (Movie_ID, Rating) VALUES (?, ?)"
   rows_modified = datatier.perform_action(dbConn, sql, [movie_id, rating])
   if rows_modified == 1:
      return 1
   else:
      return 0



##################################################################
#
# set_tagline:
#
# Sets the tagline, i.e. summary, for the given movie.
# If the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline.
# It is considered an error if the movie does not exist, and 
# the tagline is not set.
#
# Returns: 1 if the tagline was successfully set, or
#          0 if not (e.g. if the movie does not exist, or
#                    if an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
   check_movie_sql = "SELECT 1 FROM movies WHERE movie_id = ?"
   movie_row = datatier.select_one_row(dbConn, check_movie_sql, [movie_id])

   if movie_row == () or movie_row is None:
      return 0
   
   check_tagline_sql = "SELECT 1 FROM Movie_Taglines WHERE Movie_ID = ?"
   existing_tagline = datatier.select_one_row(dbConn, check_tagline_sql, [movie_id])
    
   if existing_tagline:
      #If a tagline exists, we update it
      update_sql = "UPDATE Movie_Taglines SET Tagline = ? WHERE Movie_ID = ?"
      rows_modified = datatier.perform_action(dbConn, update_sql, [tagline, movie_id])
   else:
      #If no tagline exists, then insert the new tagline
      insert_sql = "INSERT INTO Movie_Taglines (Movie_ID, Tagline) VALUES (?, ?)"
      rows_modified = datatier.perform_action(dbConn, insert_sql, [movie_id, tagline])

   if rows_modified == 1:
      return 1
   else:
      return 0
