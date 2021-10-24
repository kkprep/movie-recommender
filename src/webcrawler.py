from movie import Movie
from handleCSV import HandleCSV
import traceback

LIMIT = 100_000 # total number of movies to gather data on

# various seeds from which we will start webcrawling from
seed1 = "https://www.imdb.com/title/tt0455944/" # action
seed2 = "https://www.imdb.com/title/tt0172495/" # adventure
seed3 = "https://www.imdb.com/title/tt6977338/" # comedy
seed4 = "https://www.imdb.com/title/tt0068646/" # crime
seed5 = "https://www.imdb.com/title/tt0120338/" # drama
seed6 = "https://www.imdb.com/title/tt0241527/" # fantasy
seed7 = "https://www.imdb.com/title/tt0108052/" # history
seed8 = "https://www.imdb.com/title/tt0081505/" # horror
seed9 = "https://www.imdb.com/title/tt0055614/" # musical
seed10 = "https://www.imdb.com/title/tt0166924/" # mystery
seed11 = "https://www.imdb.com/title/tt0098635/" # romance
seed12 = "https://www.imdb.com/title/tt0062622/" # sci-fi
seed13 = "https://www.imdb.com/title/tt0120815/" # war

queue = [seed1, seed2, seed3,
         seed4, seed5, seed6,
         seed7, seed8, seed9,
         seed10, seed11, seed12,
         seed13] # ...

check = open("check.txt", 'r') # used as an emergency break

csv = HandleCSV("movies.csv")
i = 0
while len(queue) != 0:
    try:
        url = queue[0]
        if i == LIMIT:
            break
        elif i % 100 == 0: # for every 100 movies...
            text = check.readlines()[0].upper()
            if text != "CONTINUE":
                break
            check.seek(0)
            print(f"{i} movies complete!")

        try:
            movie = Movie(url, csv)
            if movie.repeat == False:
                queue += movie.findSimilar()
        except Exception as e:
            print(f"Processing of \"{url}\" failed:")
            print(f"{e}")
            traceback.print_exc()
            print("\n")

        queue.pop(0)

        i += 1
    except Exception as e:
        print("Oops, something went wrong:")
        print(f"{e}")
        traceback.print_exc()
        print("\n")

        print("***DUMPING DATA TO CSV PREMATURELY***")
        break

csv.writeToCSV() # dump data
check.close()