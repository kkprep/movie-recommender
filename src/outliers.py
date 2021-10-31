from sklearn.linear_model import RANSACRegressor
from handleCSV import HandleCSV
import pandas as pd
from ast import literal_eval
import traceback

# create multidimensional regression

class Outliers():
    def __init__(self, csv: HandleCSV):
        self.df = csv.df.copy()

    # utilizes 1.5xIQR rule
    def calculateBounds(self, data) -> tuple:
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)

        iqr = q3 - q1
        lowerBound = q1 - (1.5 * iqr)
        upperBound = q3 + (1.5 * iqr)

        return lowerBound, upperBound

    def rating(self):
        data = self.df["rating"]
        lowerBound, upperBound = self.calculateBounds(data)

        # remove outliers
        self.df = self.df[self.df["rating"] > lowerBound]
        #self.df = self.df[self.df["rating"] < upperBound]

    def numOfRatings(self):
        data = self.df["numOfRatings"]
        lowerBound, upperBound = self.calculateBounds(data)

        # remove outliers
        self.df = self.df[self.df["numOfRatings"] > lowerBound]
        #self.df = self.df[self.df["numOfRatings"] < upperBound]

    def popularity(self):
        data = self.df["popularity"]
        lowerBound, upperBound = self.calculateBounds(data)

        # remove outliers
        self.df = self.df[self.df["popularity"] > lowerBound]
        #self.df = self.df[self.df["popularity"] < upperBound]

    """ TODO: this function contains critical bugs """
    # def numOfAwards(self):
    #     # THE FOLLOWING CODE WAS COPIED FROM "plot.py"
    #     # evaluate to list
    #     self.df = self.df[self.df["numOfAwards"].notnull()]
    #     self.df["numOfAwards"] = list(map(literal_eval, self.df["numOfAwards"]))

    #     # convert each item to <int>
    #     i = 0
    #     while True:
    #         try:
    #             if i >= len(self.df.index):
    #                 break
    #             item = self.df.iloc[i, 5] # '5' corresponds to <numOfRatings>
    #             self.df.iloc[i, 5] = str(map(int, item))
    #             i += 1
    #         except:
    #             traceback.print_exc()
    #             self.df.drop(self.df.index[[i]], inplace=True)

    #     wins = pd.DataFrame(columns=["Wins"])
    #     nominations = pd.DataFrame(columns=["Nominations"])
    #     i = 0
    #     for item in self.df["numOfAwards"]:
    #         try:
    #             itemList = list(map(literal_eval, item))
    #             wins.loc[i] = int(itemList[0])
    #             nominations.loc[i] = int(itemList[1])
    #             i += 1
    #         except:
    #             self.df.drop(self.df.index[[i]], inplace=True)
    #             continue

    #     # remove outliers
    #     lowerBoundWins, upperBoundWins = self.calculateBounds(wins)
    #     lowerBoundNominations, upperBoundNominations = self.calculateBounds(nominations)

    #     self.df = self.df[wins["Wins"] > lowerBoundWins]
    #     #self.df = self.df[wins["Wins"] < upperBoundWins]

    #     self.df = self.df[nominations["Nominations"] > lowerBoundNominations]
    #     #self.df = self.df[nominations["Nominations"] < upperBoundNominations]

    def yearMade(self):
        data = self.df["yearMade"]
        lowerBound, upperBound = self.calculateBounds(data)

        # remove outliers
        self.df = self.df[self.df["yearMade"] > lowerBound]
        #self.df = self.df[self.df["yearMade"] < upperBound]

    def length(self):
        data = self.df["length"]
        lowerBound, upperBound = self.calculateBounds(data)

        # remove outliers
        self.df = self.df[self.df["length"] > lowerBound]
        self.df = self.df[self.df["length"] < upperBound]

    def gross(self):
        data = self.df["gross"]
        lowerBound, upperBound = self.calculateBounds(data)

        # remove outliers
        self.df = self.df[self.df["gross"] > lowerBound]
        #self.df = self.df[self.df["gross"] < upperBound]

if __name__ == "__main__":
    csv = HandleCSV("movies.csv")
    removeOutliers = Outliers(csv)

    length = len(removeOutliers.df.index)
    diff = length
    print(f"Number of movies BEFORE: {length}")

    removeOutliers.rating()
    removeOutliers.numOfRatings()
    removeOutliers.popularity()
    #removeOutliers.numOfAwards()
    removeOutliers.yearMade()
    removeOutliers.length()

    length = len(removeOutliers.df.index)
    diff -= length
    print(f"Number of movies AFTER: {length}")
    print(f"Number of movies REMOVED: {diff}")