import pandas as pd
from pandas.io.parsers import TextFileReader

class HandleCSV():
    def __init__(self, filename):
        self.df = pd.read_csv(filename)

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