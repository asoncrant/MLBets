from .nflScraper import nflScraper
from .utils.gameUtils import utils
from bs4 import BeautifulSoup
import html5lib, lxml, requests, time
import pandas as pd

class gmScraper(nflScraper):
    """Base web-scraping class for NFL games."""

    def __init__(self, config=None):
        self.url = config.url
        self.years = config.years
        self.weeks = config.weeks
        self.wait = config.wait

    def run(self):
        """Collect game data using utility functions"""

        games = pd.DataFrame()
        for year in self.years:
            link = utils.getLink(self.url, year)
            table = utils.getTable(link)
            frame = utils.getGames(table, year, self.weeks)

            games = games.append(frame, ignore_index = True)

            time.sleep(3)

        return games
