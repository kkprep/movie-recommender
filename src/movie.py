import requests
from bs4 import BeautifulSoup

class Movie():
    def __init__(self, url: str):
        self.attributes = {}

        # add check to verify the domain is "imdb.com"
        self.url = url
        self.webScrape()

    def setMovie(self, url: str):
        # add check to verify the domain is "imdb.com"
        self.url = url
        self.webScrape()

    def webScrape(self):
        # may need to add try-except block
        page = requests.get(self.url) # get page HTML through request
        soup = BeautifulSoup(page.content, "html.parser") # parse content
        
        self.attributes["title"] = soup.select(".TitleHeader__TitleText-sc-1wu6n3d-0")
        self.attributes["rating"] = soup.select(".AggregateRatingButton__RatingScore-sc-1ll29m0-1")
        self.attributes["numOfRatings"] = soup.select(".AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3")
        self.attributes["popularity"] = soup.select(".TrendingButton__TrendingScore-bb3vt8-1")
        self.attributes["numOfAwards"] = soup.select("li[data-testid=\"award_information\"] div ul li span")
        self.attributes["parentalRating"] = soup.select(".TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 ul li a")
        self.attributes["yearMade"] = soup.select(".TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 ul li a")
        self.attributes["genre"] = soup.select("div[data-testid=\"genres\"] a span")
        self.attributes["language"] = soup.select("li[data-testid=\"title-details-languages\"] div ul li a")
        self.attributes["length"] = soup.select("li[data-testid=\"title-techspec_runtime\"] div ul li span")
        self.attributes["gross"] = soup.select("li[data-testid=\"title-boxoffice-cumulativeworldwidegross\"] div ul li span")
        # ...

        self.parse()

    """ format attributes """
    def parse(self):
        # title
        if len(self.attributes["title"]) == 0:
            self.attributes["title"] = None
        else:
            self.attributes["title"] = str(self.attributes["title"][0].text)

        # rating
        if len(self.attributes["rating"]) == 0:
            self.attributes["rating"] = None
        else:
            self.attributes["rating"] = float(self.attributes["rating"][0].text)

        # numOfRatings
        if len(self.attributes["numOfRatings"]) == 0:
            self.attributes["numOfRatings"] = None
        else:
            self.attributes["numOfRatings"] = str(self.attributes["numOfRatings"][0].text).lower()
            if 'k' in self.attributes["numOfRatings"]:
                self.attributes["numOfRatings"] = int(self.attributes["numOfRatings"][:-1]) * 1000
            self.attributes["numOfRatings"] = int(self.attributes["numOfRatings"])

        # popularity
        if len(self.attributes["popularity"]) == 0:
            self.attributes["popularity"] = None
        else:
            self.attributes["popularity"] = self.attributes["popularity"][0].text
            self.attributes["popularity"] = int(self.attributes["popularity"].replace(',', ""))

        # numOfAwards
        if len(self.attributes["numOfAwards"]) == 0:
            self.attributes["numOfAwards"] = None
        else:
            self.attributes["numOfAwards"] = str(self.attributes["numOfAwards"][0].text)

            wins = self.attributes["numOfAwards"].find("wins")
            if wins == -1:
                wins = 0
            else:
                wins = int(self.attributes["numOfAwards"][:wins - 1])

            nominations = self.attributes["numOfAwards"].find("nominations")
            if nominations == -1:
                nominations = 0
            else:
                if wins == 0: # "x wins" does not exist in string
                    nominations = self.attributes["numOfAwards"][:nominations - 1]
                else:
                    start = self.attributes["numOfAwards"].find("&") + 2
                    nominations = int(self.attributes["numOfAwards"][start:nominations - 1])
            
            self.attributes["numOfAwards"] = [wins, nominations]

        # parentalRating
        if len(self.attributes["parentalRating"]) == 0:
            self.attributes["parentalRating"] = None
        else:
            self.attributes["parentalRating"] = str(self.attributes["parentalRating"][1].text)

        # yearMade
        if len(self.attributes["yearMade"]) == 0:
            self.attributes["yearMade"] = None
        else:
            self.attributes["yearMade"] = int(self.attributes["yearMade"][0].text)

        # genre
        if len(self.attributes["genre"]) == 0:
            self.attributes["genre"] = None
        else:
            # there might be multiple genres!
            temp = []
            for element in self.attributes["genre"]:
                temp.append(str(element.text))
            self.attributes["genre"] = temp

        # language
        if len(self.attributes["language"]) == 0:
            self.attributes["language"] = None
        else:
            # there might be multiple languages!
            temp = []
            for element in self.attributes["language"]:
                temp.append(str(element.text))
            self.attributes["language"] = temp

        # length
        if len(self.attributes["length"]) == 0:
            self.attributes["length"] = None
        else:
            self.attributes["length"] = str(self.attributes["length"][0].text)
            
            hours = self.attributes["length"].find('h')
            if hours == -1:
                hours = 0
            else:
                hours = int(self.attributes["length"][:hours])
            
            minutes = self.attributes["length"].find("min")
            if minutes == -1:
                minutes = 0
            else:
                if hours == 0: # "h" doesn't exist
                    minutes = int(self.attributes["length"][:minutes])
                else:
                    start = self.attributes["length"].find('h') + 2
                    minutes = int(self.attributes["length"][start:minutes])

            self.attributes["length"] = (hours * 60) + minutes # total number of minutes

        # gross
        if len(self.attributes["gross"]) == 0:
            self.attributes["gross"] = None
        else:
            self.attributes["gross"] = str(self.attributes["gross"][0].text)

            self.attributes["gross"] = self.attributes["gross"].replace(',', "")
            self.attributes["gross"] = int(self.attributes["gross"].replace('$', ""))

    def setAttribute(self, attribute: str, value):
        # may need to include try-except block
        self.attributes[attribute] = value

    def getAttribute(self, attribute: str):
        # may need to include try-except block
        return self.attributes[attribute]

    def prettyPrint(self):
        # header
        text = "Here's what I found about \"{}\" on IMDb:".format(self.attributes["title"])
        length = len(text)
        print(text)
        print(('_' * length) + '\n')

        print("Title: {}".format(self.attributes["title"]))
        print("Rating (_/10): {}".format(self.attributes["rating"]))
        print("Number of Ratings: {}".format(self.attributes["numOfRatings"]))
        print("Popularity (see IMDb): {}".format(self.attributes["popularity"]))
        print("Number of Awards [wins, nominations]: {}".format(self.attributes["numOfAwards"]))
        print("Parental Rating: {}".format(self.attributes["parentalRating"]))
        print("Made in: {}".format(self.attributes["yearMade"]))
        print("Genre(s): {}".format(self.attributes["genre"]))
        print("Language(s): {}".format(self.attributes["language"]))
        print("Length: {} minutes".format(self.attributes["length"]))
        print("Gross Worldwide: ${}".format(self.attributes["gross"]))