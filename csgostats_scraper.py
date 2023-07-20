from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import re
import sys
op = webdriver.ChromeOptions()

#Uses selenium to obtain stats from csgostats.gg
def scrape_profile(player_profile):
    chromedriver_path = '/usr/bin/chromedriver'
    driver = webdriver.Chrome(service=Service(chromedriver_path), options = op)
    url = player_profile + '?type=comp&date_start=1689458400&date_end=#/matches'
    driver.get(url)

    #Getting the player stats meta tag
    game_data_table_body = driver.find_element(By.XPATH,"//tbody")
    game_data_table_rows = game_data_table_body.find_elements(By.XPATH, "//tr[@class='p-row js-link ']")

    game_data_complete = []
    for i in game_data_table_rows:
        game_data = []
        data = i.find_elements(By.CLASS_NAME, "col-stats")
        for j in data:
            if j.text == "":
                continue
            game_data.append(j.text)

        game_data_complete.append(game_data)
    #Getting the total number of games played


    #Using javascript to find the player rank, wouldn't load properly with find_element
    rank_image_url = driver.execute_script("return document.querySelector('div.player-ranks img').getAttribute('src')")
    #Format used to insert image to cell and resize to fit the cell
    rank_image_cell_text = f"=IMAGE(\"{rank_image_url}\")"
    
    driver.quit()
    return game_data_complete, rank_image_cell_text

#Using regular expressions to exract each individual stat into a variable which is returned in tuple format
def get_stats(game_data_complete, rank_image_cell_text):#
    array_length = len(game_data_complete)
    if game_data_complete is not None:
        kills = []
        deaths = []
        assists = []
        hs_percentage = []
        adr = []
        for x, data in enumerate(game_data_complete):
            kills.append(game_data_complete[x][0])
            deaths.append(game_data_complete[x][1])
            assists.append(game_data_complete[x][2])
            hs_percentage.append(game_data_complete[x][4])
            adr.append(game_data_complete[x][5])
        return (kills, deaths, assists, hs_percentage, adr)
