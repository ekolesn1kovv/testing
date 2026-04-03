import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv('api_url')


def get_heroes():
    response = requests.get(api_url, timeout=5)
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Неверный формат данных")

    return data


def hero_has_work(hero):
    occupation = hero.get("work", {}).get("occupation")

    if not isinstance(occupation, str):
        return False

    occupation = occupation.strip()
    return occupation not in ("", "-")


def height_cm(hero):
    heights = hero.get("appearance", {}).get("height")

    if not isinstance(heights, list):
        return None

    for value in reversed(heights):
        if not isinstance(value, str):
            continue

        match = re.search(r"(\d+)\s*cm", value)
        if match:
            return int(match.group(1))

    return None


def tallest_hero(heroes, gender, has_work):
    filtered = []

    for hero in heroes:
        hero_gender = hero.get("appearance", {}).get("gender")
        current_has_work = hero_has_work(hero)
        hero_height = height_cm(hero)

        if hero_gender == gender and current_has_work == has_work and hero_height is not None:
            filtered.append(hero)

    if not filtered:
        raise ValueError("Герой не найден")

    return max(filtered, key=height_cm)


def find_tallest_hero(gender, has_work):
    if not isinstance(gender, str):
        raise TypeError("Неверный формат данных - gender")

    if not isinstance(has_work, bool):
        raise TypeError("Неверный формат данных - has_work")

    gender = gender.strip()

    if gender not in ("Male", "Female"):
        raise ValueError("Ошибка значения")

    heroes = get_heroes()
    return tallest_hero(heroes, gender, has_work)