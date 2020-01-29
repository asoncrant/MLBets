from bs4 import BeautifulSoup
import html5lib, lxml, requests, time
import pandas as pd

class utils(object):
    """
    Class of utility functions for extracting NFL game data.
    """

    @staticmethod
    def getLink(link, year):
        """
        Locate table for games in specified year.
        """

        return link.format(year)

    @staticmethod
    def getTable(link):
        """
        Extract table, in HTML, from link.
        """
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")

        table = soup.find('table', {'class': "sortable stats_table"})

        return table


    @staticmethod
    def getInfo(link):
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        for c in comments:
            if re.search("game_info", c):
                table = BeautifulSoup(c, "html.parser")
                break

        info = pd.read_html(str(table), header=0, index_col=0)[0].T.to_dict(orient="records")[0]

        if "Won OT Toss" in info.keys():
            del info["Won OT Toss"]
        if "Weather" not in info.keys():
            info["Weather"] = ""

        time.sleep(3)

        return info

    @staticmethod
    def getInfoLink(htmlVal):
        """Get link to info table from html val attribute"""

        beg = "https://www.pro-football-reference.com/"
        end = htmlVal.find('a')['href']

        return beg + end

    @staticmethod
    def getGames(table, year, weeks=None):
        """
        Get game data from link.
        """

        games = {}
        games["year"] = []
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            week = row.find('th')
            if week.text in ["Week", ""]:
                continue
            skip = False
            if weeks:
                if int(week.text) in weeks:
                    stats = row.find_all('td')
                else:
                    skip = True
            else:
                stats = row.find_all('td')

            if skip:
                continue

            else:
                games["year"].append(year)
                try:
                    games[week['data-stat']].append(week.text)
                except KeyError:
                    games[week['data-stat']] = [week.text]

                for stat in stats:
                    if stat['data-stat'] == "boxscore_word":
                        try:
                            infoLink = getInfoLink(stat)
                        except TypeError:
                            continue

                        info = getInfo(infoLink)
                        for key in info.keys():
                            try:
                                games[key].append(info[key])
                            except KeyError:
                                games[key] = [info[key]]
                    else:
                        try:
                            games[stat['data-stat']].append(stat.text)
                        except KeyError:
                            games[stat['data-stat']] = [stat.text]

        frame = pd.DataFrame.from_dict(games)
