import json
from scrapers.posScraper import qbScraper, rushScraper, recScraper
from docs.position.config import posnConfig


def setConfig():
    with open('docs/position/config.json') as config_file:
        raw_config = json.load(config_file)
    posn_config = posnConfig(raw_config)
    return posn_config

def runAll(posn_config):
    qb = qbScraper(posn_config)
    rush = rushScraper(posn_config)
    rec = recScraper(posn_config)

    qbStats = qb.run()
    rushStats = rush.run()
    recStats = rec.run()

    fin = [qbStats, rushStats, recStats]

    return fin


if __name__ == "__main__":
    posn_config = setConfig()
    runAll(posn_config)
