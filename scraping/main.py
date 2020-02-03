from scrapers.posnScraper import qbScraper, rushScraper, recScraper
from scrapers.gameScraper import gmScraper
from docs.position.config import posnConfig
from docs.game.config import gameConfig
import pandas as pd
import json, os, sqlalchemy, time

user = os.environ['USERNAME']
pw = os.environ['PASSWORD']
db = os.environ['DB']

engine_string = "postgresql://{user}:{pw}@database:5432/{db}".format(user=user, pw=pw, db=db)\

def setConfig():
    with open('./scraping/docs/config.json') as config_file:
        raw_config = json.load(config_file)
    posn_config = posnConfig(raw_config)
    game_config = gameConfig(raw_config)
    return posn_config, game_config

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
    posn_config, game_config = setConfig()

    print(posn_config)
    print(game_config)

    print("SUCCESSFULLY MOUNTED VOLUME")

    results = runAll(posn_config, game_config)
    engine = sqlalchemy.create_engine(engine_string)

    attempts = 0
    while attempts < 10:
        attempts += 1
        try:
            con = engine.connect()
            if con:
                break
        except:
            time.sleep(.5)

    if not con:
        print("connection could not be  established")

    for df in results.keys():
        results[df].to_sql(df, engine, if_exists='append', index=False)
    con.close()
