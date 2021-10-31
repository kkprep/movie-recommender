# implement k-nearest neighbors (knn) algroithm
from movie import Movie
from handleCSV import HandleCSV
import numpy as np

# given a movie, outputs 5 similar movies
url = input("Enter IMDb url of a movie you enjoy: ")
csv = HandleCSV("temp.csv")

movie = Movie(url, csv)
attributes = [movie.attributes["numOfRatings"], movie.attributes["popularity"], movie.attributes["gross"], movie.attributes["rating"]]

# FIXED ==> [CRITICAL BUG] NEED TO NORMALIZE THE ATTRIBUTES
###################### BAD - DUPLICATE CODE FROM NORMALIZATION.PY ##########################################
fp = open("inliers", "rb")
data = np.load(fp, allow_pickle=True)

# 4 features: rating, numOfRatings, popularity, gross
numOfRatings = data[:, 0]
numOfRatings = numOfRatings[0]
maxNumOfRatings = np.amax(numOfRatings)
minNumOfRatings = np.amin(numOfRatings)

popularity = data[:, 0]
popularity = popularity[1]
maxPopularity = np.amax(popularity)
minPopularity = np.amin(popularity)

gross = data[:, 0]
gross = gross[2]
maxGross = np.amax(gross)
minGross = np.amin(gross)

rating = data[:, 1]
maxRating = np.amax(rating)
minRating = np.amin(rating)

# normalize data (between 0 and 1, inclusive)
# xnorm = (xi - xmin) / (xmax - xmin)
for i in range(len(attributes)):
    attributes[i] = (attributes[i] - minNumOfRatings) / (maxNumOfRatings - minNumOfRatings)

#######################################################################################################

fp = open("normalized", "rb")
data = np.load(fp, allow_pickle=True)
distances = {} # index:distance
for i in range(len(data)):
    dataNumOfRatings = data[i][0][0]
    dataPopularity = data[i][0][1]
    dataGross = data[i][0][2]
    dataRating = data[i][1]
    d = ((dataNumOfRatings - attributes[0])**2 + (dataPopularity - attributes[1])**2 + (dataGross - attributes[2])**2 + (dataRating - attributes[3])**2)**(1.0/2.0)
    distances[i] = d

sortedDistances = dict(sorted(distances.items(), key=lambda x:x[1]))
sortedDistances = list(sortedDistances.keys())
print("Here are the most similar movies I could find:")
print("----------------------------------")
for i in range(5):
    # print 5 most similar movies
    print(str(data[sortedDistances[i], 2]))
    print("----------------------------------")