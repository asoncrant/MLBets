from bs4 import BeautifulSoup
from ..nflScraper import nflScraper
import html5lib, lxml, requests, time
import pandas as pd

class utils(object):
    """Utility functions for scraping player data"""

    @staticmethod
    def getLink(url, year, week, id):
        """
        Locate the link of the table for position
        in specified year and week.
        """
        week_url = url.format(year, week) # format url

        page = requests.get(week_url) # get base html from base url
        soup = BeautifulSoup(page.text, 'html.parser')

        # find link to stats
        link_end = soup.find("div", {'id': id}).find('a')['href']
        link = nflScraper.domain + link_end

        return link

    @staticmethod
    def getTable(link):
        """Identify the table (in HTML) for position."""
        page = requests.get(link) # get HTML for stats
        soup = BeautifulSoup(page.text, 'html.parser')
        # find stats table
        table = soup.find('table', {'class': "sortable stats_table"})

        return table

    @staticmethod
    def getStats(table):
        """Extract all statistics for every player at this position."""
        stats = {}
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            rank = row.find("th")
            if rank.text == "Rk":
                continue
            else:
                try:
                    stats[rank["data-stat"]].append(rank.text)
                except KeyError:
                    stats[rank["data-stat"]] = [rank.text]

            cats = row.find_all("td")
            for cat in cats:
                try:
                    stats[cat["data-stat"]].append(cat.text)
                except KeyError:
                    stats[cat["data-stat"]] = [cat.text]

        frame = pd.DataFrame.from_dict(stats)

        return frame
