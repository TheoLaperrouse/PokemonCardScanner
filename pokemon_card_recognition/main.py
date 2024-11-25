from .card_matcher import match_cards
from .card_detector import detect_cards, load_reference_cards
from .card_infos import save_cards_info
import os
import asyncio
from inference_sdk import InferenceHTTPClient
from dotenv import dotenv_values

config = dotenv_values(".env")


async def recognize_cards():
    roboflow_client = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=config['ROBOFLOW_API_KEY']
    )
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(script_dir, '..')
    image_path = os.path.join(root_dir, 'cards.jpeg')
    reference_dir = os.path.join(root_dir, 'cards')
    output_dir = os.path.join(root_dir, 'detected_cards')
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = roboflow_client.infer(
            image_path, model_id="pokemoncarddetector/4")
        detected_cards = detect_cards(result, image_path, output_dir)

        reference_cards = load_reference_cards(reference_dir)
        matches = match_cards(detected_cards, reference_cards)

        ids = [
            f"{extension}-{card.split('_')[0]}" for match in matches for extension, card in [match.split(' : ')]]
        await save_cards_info(ids)
    except Exception as e:
        print(f"Erreur lors de l'inférence : {e}")


if __name__ == "__main__":
    asyncio.run(recognize_cards())
