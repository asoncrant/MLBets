from bs4 import BeautifulSoup
import requests, lxml, html5lib
import pandas as pd

class nflScraper(object):
    """
    Base class for web scraping NFL data.
    Basic operations are:
       1. find a link
       2. find a table
       3. extract information from table.
    """

    domain = "https://www.pro-football-reference.com"

    def __init__(self):
        raise NotImplementedError

    def getLink(self):
        """Identify table link"""

        raise NotImplementedError

    def getTable(self):
        """Identify the table (in HTML)"""

        raise NotImplementedError

    def getStats(self):
        """Extract all statistics from the table"""

        raise NotImplementedError
