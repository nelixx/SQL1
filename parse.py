import requests
from bs4 import BeautifulSoup
from database import Database

def get_game(games_title: str):
    correct_title = games_title.replace(' ', '%20').strip() 
    response = requests.get(url)
    url = f'https://game-shop.com.ua/ua={correct_title}'
   
    soup = BeautifulSoup(response.content, 'html.parser')
   
    games_soup = soup.select('.category-card.category-layout')
    result = []


    x = 0
    for games in games_soup:
        x += 1
        title = games.select_one('.ui-card-title.category-card__name').text.strip()
        author = games.select_one('.creator-label').text.strip()
        availability = games.select_one('.ui-shipment-status > span')
        if availability:
            availability = availability.text.strip()
        else:
            availability = games.select_one('.ui-display-games-type > span').text.strip()
        relative_games_url ='https://game-shop.com.ua/ua{relative_games_url}'
        poster = games.select_one('.product-image > img').get('src')

        games_obj = {
        'title' : title,
        'author' : author,
        'availability' : availability,
        'url' : games_url,
        'banner': poster
        }

        result.append(games_obj)
        if x > 5:
            break

    return result