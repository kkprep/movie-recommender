from movie import Movie

# Proof of Concept

theImitationGame = "https://www.imdb.com/title/tt2084970/"

# url = input("Please type IMDb URL of movie: ")
url = theImitationGame

movie = Movie(url)
movie.prettyPrint()