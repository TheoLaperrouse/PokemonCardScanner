# Pokemon Card Recognition

Recognize and evaluate price of Pokemon cards from pictures

## Quick start

Add an env variable :

```
ROBOFLOW_API_KEY=YOUR_API_KEY
```

Add a picture to root folder (`cards.jpeg`)

Run :

```sh
poetry install && poetry run python -m pokemon_card_recognition.main
```

Retrieve all the informations in `card_infos.csv`