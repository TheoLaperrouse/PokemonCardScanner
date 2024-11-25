import os
import requests

set = 'neo2'
folder_name = f'cards/{set}'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

api_url = f"https://api.tcgdex.net/v2/fr/sets/{set}"
response = requests.get(api_url).json()
cards = response['cards']

for card in cards:
    card_name = card['name'].replace(" ", "_")
    image_url = f'{card["image"]}/high.png'
    image_data = requests.get(image_url).content
    local_id = card['localId']
    with open(f"{folder_name}/{local_id}_{card_name}.png", "wb") as img_file:
        img_file.write(image_data)
