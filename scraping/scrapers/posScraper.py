from .nflScraper import nflScraper
from bs4 import BeautifulSoup
import html5lib, lxml, requests, time
import pandas as pd

class posScraper(nflScraper):
    """Base web scraping class for position players."""

    def __init__(self, config=None, position=None):
        self.id = config.pos_ids[position]
        self.years = config.years
        self.weeks = config.weeks
        self.url = config.url
        self.table_class = config.table_class
        self.wait = config.wait

    def getLink(self, year, week):
        """
        Locate the link of the table for position
        in specified year and week.
        """
        week_url = self.url.format(year, week) # format url

        page = requests.get(week_url) # get base html from base url
        soup = BeautifulSoup(page.text, 'html.parser')

        # find link to stats
        link_end = soup.find("div", {'id':self.id}).find('a')['href']
        link = self.domain + link_end

        return link

    def getTable(self, link):
        """Identify the table (in HTML) for position."""
        table_page = requests.get(link) # get HTML for stats
        table_soup = BeautifulSoup(table_page.text, 'html.parser')
        # find stats table
        table = table_soup.find('table', {'class': 'sortable stats_table'})

        return table

    def getStats(self, table):
        """Extract all statistics for every player at this position."""
        stats = {}
        # for every statistical category
        for cat in table.find_all("th",{"scope": "col"}):
            catName = cat['data-stat'] # name of category
            stats[catName] = []
            for val in table.find_all("td",{'data-stat':catName}):
                stats[catName].append(val.text)
            if len(stats[catName]) == 0: # not all categories get populated
                del stats[catName]

        frame = pd.DataFrame.from_dict(stats)

        return frame

    def run(self):
        """Collect data."""
        stats = pd.DataFrame()
        for year in self.years:
            for week in self.weeks:
                link = self.getLink(year, week)
                table = self.getTable(link)
                frame = self.getStats(table)

                stats = stats.append(frame, ignore_index=True)
                time.sleep(self.wait)

        return stats

class qbScraper(posScraper):
    """Web scraping class for quarterbacks"""

    def __init__(self, config):
        """Web crawler for weekly quarterback stats."""
        super().__init__(config=config, position='qb')

class recScraper(posScraper):
    """Web scraping class for receiving stats."""

    def __init__(self, config):
        super().__init__(config=config, position='rec')

class rushScraper(posScraper):
    """Web scraping class for rushing stats"""

    def __init__(self, config):
        super().__init__(config=config, position='rush')
