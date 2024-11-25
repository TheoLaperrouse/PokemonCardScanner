from tcgdexsdk import TCGdex
from pokemontcgsdk import Card
import csv
import asyncio

tcg_dex = TCGdex("fr")


def get_card_price(name):
    card = Card.find(name)
    avg30 = card.cardmarket.prices.averageSellPrice
    return {"avg_30": avg30}


async def get_card_infos(name):
    card = await tcg_dex.card.get(name)
    card_name = card.name
    set_name = card.set.name
    card_id = card.localId
    return {"id": card_id, "set_name": set_name, "card_name": card_name}


async def get_cards_info(card_names):
    card_infos = []
    for name in card_names:
        price_data = get_card_price(name)
        card_details = await get_card_infos(name)

        card_id = card_details["id"]
        set_name = card_details["set_name"]
        card_name = card_details["card_name"]
        avg_price = price_data["avg_30"]

        card_infos.append({
            "name": card_name,
            "set": set_name,
            "id": card_id,
            "avg_price": avg_price,
        })

    card_infos.sort(key=lambda x: x["avg_price"], reverse=True)
    return card_infos


async def save_cards_info(card_names):
    sorted_cards = await get_cards_info(card_names)

    filename = "cards_info.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Nom de la carte", "Set", "ID", "Prix moyen (€)"])

        for card in sorted_cards:
            writer.writerow([card["name"], card["set"],
                            card["id"], card["avg_price"]])

    print(f"Informations des cartes sauvegardées dans {filename}.")

    for card in sorted_cards:
        print(
            f"{card['name']} ({card['set']} n°{card['id']}) : Prix moyen : {card['avg_price']} €")
