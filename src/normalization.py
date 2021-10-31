import numpy as np

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
for i in range(len(data)):
    data[i][0][0] = (data[i][0][0] - minNumOfRatings) / (maxNumOfRatings - minNumOfRatings)
    data[i][0][1] = (data[i][0][1] - minPopularity) / (maxPopularity - minPopularity)
    data[i][0][2] = (data[i][0][2] - minGross) / (maxGross - minGross)
    data[i][1] = (data[i][1] - minRating) / (maxRating - minRating)

fp = open("normalized", "wb")
np.save(fp, data)
fp.close()

print(data)