import requests
from django.conf import settings
from django.db import IntegrityError

from characters.models import Characters


def scrape_characters() -> list[Characters]:

    next_url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL

    characters = []

    while next_url_to_scrape is not None:
        characters_response = requests.get(next_url_to_scrape).json()

        for character_dict in characters_response["results"]:
            characters.append(Characters(
                api_id=character_dict["id"],
                name=character_dict["name"],
                status=character_dict["status"],
                species=character_dict["species"],
                gender=character_dict["gender"],
                image=character_dict["image"],
            ))
        next_url_to_scrape = characters_response["info"]["next"]
    return characters


def save_characters(characters: list[Characters]) -> None:
    for character in characters:
        try:
            character.save()
        except IntegrityError:
            print(f"Character with this api_id: {character.api_id} already exists")


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
