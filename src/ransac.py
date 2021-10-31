# implement RANdom SAmple Concenus (RANSAC) algorithm to detect and remove outliers
from handleCSV import HandleCSV
from numpy import array
import numpy as np
import pandas as pd
import time
from ast import literal_eval
import traceback

import warnings
warnings.filterwarnings("ignore")

csv = HandleCSV("movies.csv")

from sklearn.linear_model import LinearRegression

def ransac(csv: HandleCSV):
    iterations = 0
    bestFit = None
    bestErr = float("inf")
    allInliers = []

    while iterations < 20:
        maybeInliers = []
        maybeModel = None
        data = []
        x = []
        y = []

        # get 2 random points and determine best model
        while True:
            try:
                data = csv.getRandomRows(2)

                x = []
                x.append(list(data[0][["numOfRatings", "popularity", "gross"]]))
                x.append(list(data[1][["numOfRatings", "popularity", "gross"]]))
                
                y = list(data[0][["rating"]]) + list(data[1][["rating"]])

                maybeModel = LinearRegression().fit(x, y)
                maybeInliers = [[x[0], y[0], list(data[0][["url"]])], [x[1], y[1], list(data[1][["url"]])]]
                break
            except:
                continue

        # find other potential inliers in dataset
        alsoInliers = []
        for i in range(len(csv.df.index) - 1):
            try:
                point = csv.df.iloc[i]
                url = point[["url"]]
                point = point.loc[["rating", "numOfRatings", "popularity", "gross"]]
                # if point in data:
                #     continue
                actualRating = float(point[["rating"]])
                point = point[["numOfRatings", "popularity", "gross"]]
                predictedRating = float(maybeModel.predict([point])[0])
                percentError = abs((predictedRating - actualRating) / actualRating)
                #print(percentError)
                if percentError <= 0.15:
                    temp = [point.tolist()]
                    temp.append(actualRating)
                    temp.append(url)
                    alsoInliers.append(temp)
            except:
                continue
        if len(alsoInliers) > 1000:
            allInliers = maybeInliers + alsoInliers
            x = []
            y = []
            for i in range(len(allInliers)):
                try:
                    x.append(allInliers[i][0])
                    y.append(allInliers[i][1])
                except:
                    continue
            betterModel = LinearRegression().fit(x, y)
            thisErr = betterModel.score(x, y)
            if thisErr < bestErr:
                bestFit = betterModel
                bestErr = thisErr
        iterations += 1
    
    return bestFit, allInliers



bestFit, allInliers = ransac(csv)

fp = open("inliers", "wb")
allInliers = np.array(allInliers)
np.save(fp, allInliers)
fp.close()

print(bestFit.get_params())
print("\n")
print(allInliers)