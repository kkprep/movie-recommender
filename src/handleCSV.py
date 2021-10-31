import pandas as pd
from random import *
import numpy as np
import time

class HandleCSV():
    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        self.df = self.df.replace('', np.nan)

    def addRow(self, data: dict):
        index = self.df.index
        self.df.loc[len(index)] = data.values()

    """ return True if repeat, False otherwise """
    def isRepeat(self, url) -> bool:
        thisMovie = self.df[self.df["url"] == url]
        return thisMovie.shape[0] > 0

    def writeToCSV(self):
        self.df.to_csv("movies.csv", mode='a', header=False)

    def getFeature(self, feature: str):
        # warning: there is NO check to validate that <feature>
        # exists in <self.df>
        dfCopy = self.df.dropna()
        return dfCopy[feature]

    def getRandomRows(self, n: int):
        dfCopy = self.df.copy().dropna()
        length = len(dfCopy.index)
        r = []
        # there may be duplicate entires in <r>
        i = 0
        while i != n:
            seed(time.time())
            temp = dfCopy.iloc[randint(0, length - 2)]
            temp = temp.loc[["rating", "numOfRatings", "popularity", "numOfAwards", "gross", "url"]]
            r.append(temp)
            i = i + 1
            time.sleep(0.01)
                
        return r