from scrapers.posScraper import qbScraper, rushScraper, recScraper
from scrapers.gmScraper import gmScraper
from docs.position.config import posnConfig
from docs.game.config import gameConfig

import json
import pandas as pd


def setPosnConfig():
    with open('docs/position/config.json') as config_file:
        raw_config = json.load(config_file)
    posn_config = posnConfig(raw_config)
    return posn_config

def setGameConfig():
    with open('docs/game/config.json') as config_file:
        raw_config = json.load(config_file)
    game_config = gameConfig(raw_config)
    return game_config

def runPosn(posn_config):
    qb = qbScraper(posn_config)
    rush = rushScraper(posn_config)
    rec = recScraper(posn_config)

    qbStats = qb.run()
    rushStats = rush.run()
    recStats = rec.run()

    return qbStats, rushStats, recStats

def runGame(game_config):
    gms = gmScraper(game_config)

    games = gms.run()
    return games

def runAll(posn_config, game_config):
    qb, rb, rec = runPosn(posn_config)
    # games = runGame(game_config)

    return {"qb": qb, "rb": rb, "rec": rec}



if __name__ == "__main__":
    posn_config = setPosnConfig()
    game_config = setGameConfig()

    results = runAll(posn_config, game_config)

    for df in results.keys():
        results[df].to_csv("{}.csv".format(df), index=False)
