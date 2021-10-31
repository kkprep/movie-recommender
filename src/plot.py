# code to graph the data we've gathered from webcrawling
import matplotlib.pyplot as plt
from handleCSV import HandleCSV
from ast import literal_eval
import numpy as np
import definitions

class Plot():
    def __init__(self, csv: HandleCSV):
        self.csv = csv

    def prepareGeneral(self, xlabel, ylabel, title):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

    def prepareHistogram(self, feature, bins, bounds, xlabel, ylabel, title):
        plt.hist(feature, bins, bounds, histtype="bar", rwidth=0.8)
        self.prepareGeneral(xlabel, ylabel, title)

    def prepareScatterplot(self, x, y, xlabel, ylabel, title):
        plt.scatter(x, y)
        self.prepareGeneral(xlabel, ylabel, title)

    def prepareBarplot(self, x, y, xlabel, ylabel, title):
        plt.bar(x, y)
        self.prepareGeneral(xlabel, ylabel, title)

    def plotRating(self):
        feature = self.csv.getFeature("rating")
        bins: int = 10
        bounds: tuple = (0, 10)

        xlabel = "Rating"
        ylabel = "Number of Movies"
        title = "Number of Movies vs. Rating"

        self.prepareHistogram(feature, bins, bounds, xlabel, ylabel, title)
        plt.show()

    def plotNumOfRatings(self):
        feature = self.csv.getFeature("numOfRatings")
        bins: int = 30
        bounds: tuple = (0, 1_200_000)

        xlabel = "Number of Ratings"
        ylabel = "Number of Movies"
        title = "Number of Movies vs. Number of Ratings"

        self.prepareHistogram(feature, bins, bounds, xlabel, ylabel, title)
        plt.show()

    def plotPopularity(self):
        feature = self.csv.getFeature("popularity")
        bins: int = 20
        bounds: tuple = (0, 5000)

        xlabel = "Popularity"
        ylabel = "Number of Movies"
        title = "Number of Movies vs. Popularity"

        self.prepareHistogram(feature, bins, bounds, xlabel, ylabel, title)
        plt.show()

    # make a histogram of # of wins, # of nominations, total
    def plotNumOfAwards(self):
        feature = self.csv.getFeature("numOfAwards")

        # evaluate to list
        feature = list(map(literal_eval, feature))

        # convert each item to <int>
        i = 0
        while i < len(feature):
            try:
                item = feature[i]
                feature[i] = list(map(int, item))
                i += 1
            except:
                feature.remove(item)

        feature = np.array(feature).astype(int)
        wins = feature[:, 0]
        nominations = feature[:, 1]

        xlabel = "Number of Wins"
        ylabel = "Number of Nominations"
        title = "Number of Nominations vs. Number of Wins"
        self.prepareScatterplot(wins, nominations, xlabel, ylabel, title)
        plt.show()

    def plotParentalRating(self):
        feature = self.csv.getFeature("parentalRating") # treated as <pandas.dataframe>
        length = len(feature)

        data = {}
        total = 0
        for rating in definitions.parentalRatings:
            count = len(feature[feature == rating])
            data[rating] = count
            total += count
        data["Other"] = length - total

        x = data.keys()
        y = data.values()

        xlabel = "Parental Rating"
        ylabel = "Number of Movies"
        title = "Number of Movies vs. Parental Rating"
        
        self.prepareBarplot(x, y, xlabel, ylabel, title)
        plt.show()

    def plotYearMade(self):
        feature = self.csv.getFeature("yearMade")
        bins = 50
        bounds = (1920, 2021)

        xlabel = "Year Made"
        ylabel = "Number of Movies"
        title = "Number of Movies vs. Year Made"

        self.prepareHistogram(feature, bins, bounds, xlabel, ylabel, title)
        plt.show()

    def plotGenre(self):
        feature = self.csv.getFeature("genre")
        feature = list(map(literal_eval, feature))

        data = {}
        for genre in definitions.genres:
            count = 0
            for item in feature:
                if genre in item:
                    count += 1
            data[genre] = count
        
        x = data.keys()
        y = data.values()

        xlabel = "Genre"
        ylabel = "Number of Movies"
        title = "Number of Movies vs. Genre"

        self.prepareBarplot(x, y, xlabel, ylabel, title)
        plt.show()

    def plotLanguage(self):
        feature = self.csv.getFeature("language")
        feature = list(map(literal_eval, feature))

        data = {}
        for language in definitions.languages:
            count = 0
            for item in feature:
                if language in item:
                    count += 1
            data[language] = count
        
        x = data.keys()
        y = data.values()

        xlabel = "Language"
        ylabel = "Number of Movies"
        title = "Number of Movies vs. Language"

        self.prepareBarplot(x, y, xlabel, ylabel, title)
        plt.show()

    def plotLength(self):
        feature: list = self.csv.getFeature("length")
        bins = 10
        bounds = (0, 300)

        xlabel = "Length (minutes)"
        ylabel = "Number of Movies"
        title = "Number of Movies vs. Length"

        self.prepareHistogram(feature, bins, bounds, xlabel, ylabel, title)
        plt.show()

    def plotGross(self):
        feature = self.csv.getFeature("gross")
        bins = 150
        bounds = (0, 1_000_000_000)

        xlabel = "Gross (dollars)"
        ylabel = "Number of Movies"
        title = "Number of Movies vs. Gross"

        self.prepareHistogram(feature, bins, bounds, xlabel, ylabel, title)
        plt.show()

if __name__ == "__main__":
    csv = HandleCSV("movies.csv")
    plot = Plot(csv)

    plot.plotRating()
    plot.plotNumOfRatings()
    plot.plotPopularity()
    plot.plotNumOfAwards()
    plot.plotParentalRating()
    plot.plotYearMade()
    plot.plotGenre()
    plot.plotLanguage()
    plot.plotLength()
    plot.plotGross()