import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2


def load_reference_cards(reference_dir):
    reference_cards = {}
    for root, _, files in os.walk(reference_dir):
        for filename in files:
            if filename.endswith(".png"):
                card_name = f'{root.split("/")[-1]} : {os.path.splitext(filename)[0]}'
                image_path = os.path.join(root, filename)
                image = cv2.imread(image_path)
                reference_cards[card_name] = image
    return reference_cards


def detect_cards(result, image_path, output_dir):
    image = Image.open(image_path)
    detected_cards = []

    if 'predictions' in result:
        for i, prediction in enumerate(result['predictions']):
            x_center = prediction['x']
            y_center = prediction['y']
            width = prediction['width']
            height = prediction['height']

            x1 = int(x_center - (width / 2))
            y1 = int(y_center - (height / 2))
            x2 = int(x_center + (width / 2))
            y2 = int(y_center + (height / 2))

            detected_card = image.crop((x1, y1, x2, y2))
            detected_cards.append(np.array(detected_card))

            detected_card_filename = os.path.join(
                output_dir, f'card_{i + 1}.png')
            detected_card.save(detected_card_filename)
        print(f"{len(result['predictions'])} cartes détectées enregistrées")
    else:
        print("Aucune prédiction trouvée.")

    return detected_cards
