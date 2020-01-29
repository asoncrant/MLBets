from .nflScraper import nflScraper
from .utils.posnUtils import utils
from bs4 import BeautifulSoup
import html5lib, lxml, requests, time
import pandas as pd

class posnScraper(nflScraper):
    """Base web scraping class for position players."""

    def __init__(self, config=None, position=None):
        self.id = config.pos_ids[position]
        self.years = config.years
        self.weeks = config.weeks
        self.url = config.url
        self.table_class = config.table_class
        self.wait = config.wait

    def run(self):
        """Collect data."""
        stats = pd.DataFrame()
        for year in self.years:
            for week in self.weeks:
                link = utils.getLink(self.url, year, week, self.id)

                next = True
                while next:
                    table = utils.getTable(link)
                    frame = utils.getStats(table)
                    stats = stats.append(frame, ignore_index=True)

                    if utils.checkNext(link):
                        link = utils.checkNext(link)
                    else:
                        next = False

                    time.sleep(self.wait)

        return stats

class qbScraper(posnScraper):
    """Web scraping class for quarterbacks"""

    def __init__(self, config):
        """Web crawler for weekly quarterback stats."""
        super().__init__(config=config, position='qb')

class recScraper(posnScraper):
    """
    Web scraping class for receiving stats.
    """

    def __init__(self, config):
        super().__init__(config=config, position='rec')

class rushScraper(posnScraper):
    """
    Web scraping class for rushing stats.
    """

    def __init__(self, config):
        super().__init__(config=config, position='rush')
