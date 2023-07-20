import numpy as np
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import csgostats_scraper

#USER SPECIFIC
players_dict = {
    "Chrizz": "https://csgostats.gg/player/76561198059903989",
    "Monus": "https://csgostats.gg/player/76561198054753103",
    "Julezsn": "https://csgostats.gg/player/76561198050920197",
    "Ralfović": "https://csgostats.gg/player/76561198059919319",
}

#Uploads dataframe to google sheets
def upload_to_google_sheets(players_df, index, rowCount):
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']

    ###USER SPECIFIC###
    credentials = Credentials.from_service_account_file('csgo-stats-tracker-393218-e439bf6465cf.json', scopes=scopes)

    gc = gspread.authorize(credentials)

    # open a google sheet workbook
    gs = gc.open_by_key('1tZ-q8EVqJoDGJjo83IjbSTcHIRVtj_OQQ-P4aK9YfZ8')
    # select a work sheet from its name (multiple sheets inside single workbook)
    wsChrizz = gs.worksheet('Chrizz')
    wsMonus = gs.worksheet('Monus')
    wsJulezsn = gs.worksheet('Julezsn')
    wsRalfović = gs.worksheet('Ralfović')

    # list of sheets inside workbook
    worksheets = [wsChrizz, wsMonus, wsJulezsn, wsRalfović]

    set_with_dataframe(worksheet=worksheets[index], dataframe=players_df, row=rowCount, include_index=True, include_column_header = False, resize = True)

# Function used to gather all player stats
def get_all_player_info_sequential(players_dictionary):
    all_player_info = []

    for player in players_dictionary:
        profile_info = csgostats_scraper.scrape_profile(players_dictionary[player])
        player_info_scraped = csgostats_scraper.get_stats(profile_info[0], profile_info[1])
        all_player_info.append(player_info_scraped)
    return all_player_info

if __name__ == '__main__':
    all_player_info = get_all_player_info_sequential(players_dict)
    gameCount = 0
    rowCount = 1

    for player_info in np.nditer(all_player_info, flags = ['external_loop'], order = 'F'):
        gameCount += 1
        rowCount += 1
        for index, value in enumerate(player_info):
            print(index)
            print(value)
            gameIndex = 'Game ' + str(gameCount)
            players_df = pd.DataFrame([value], columns=['Kills', 'Deaths', 'Assists', 'Headshot %', 'ADR'], index=[gameIndex])
            upload_to_google_sheets(players_df, index, rowCount)