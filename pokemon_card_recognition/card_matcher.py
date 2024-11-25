import cv2


def match_cards(detected_cards, reference_cards):
    matches = []
    orb = cv2.ORB_create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    reference_descriptors = {}
    for ref_name, ref_image in reference_cards.items():
        _, descriptors = orb.detectAndCompute(ref_image, None)
        if descriptors is not None:
            reference_descriptors[ref_name] = descriptors

    for card in detected_cards:
        _, descriptors1 = orb.detectAndCompute(card, None)
        if descriptors1 is None:
            matches.append("Carte non reconnue")
            continue

        best_match = None
        max_matches = 0

        for ref_name, descriptors2 in reference_descriptors.items():
            matches_found = bf.match(descriptors1, descriptors2)
            if len(matches_found) > max_matches:
                max_matches = len(matches_found)
                best_match = ref_name

        matches.append(best_match if best_match else "Carte non reconnue")
    return matches
