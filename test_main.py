import pytest
import requests

from main import (
    api_url,
    get_heroes,
    find_tallest_hero,
    tallest_hero,
    hero_has_work,
    height_cm,
)


@pytest.fixture(scope="session")
def heroes():
    return get_heroes()


@pytest.mark.parametrize(
    "gender, has_work",
    [
        ("Male", True),
        ("Male", False),
        ("Female", True),
        ("Female", False),
    ],
)
def test_find_tallest_hero_returns_correct_hero(heroes, gender, has_work):
    result = find_tallest_hero(gender, has_work)

    assert isinstance(result, dict)
    assert result.get("appearance", {}).get("gender") == gender
    assert hero_has_work(result) is has_work
    assert height_cm(result) is not None

    expected = tallest_hero(heroes, gender, has_work)

    assert result["id"] == expected["id"]
    assert result["name"] == expected["name"]


@pytest.mark.parametrize("gender", ["male", "female", "", "Unknown", "MALE"])
def test_find_tallest_hero_invalid_gender_value(gender):
    with pytest.raises(ValueError):
        find_tallest_hero(gender, True)


@pytest.mark.parametrize("gender", [None, 123, [], {}, 1.5])
def test_find_tallest_hero_invalid_gender_type(gender):
    with pytest.raises(TypeError):
        find_tallest_hero(gender, True)


@pytest.mark.parametrize("has_work", [None, 1, 0, "true", "false", [], {}, 2.5])
def test_find_tallest_hero_invalid_has_work_type(has_work):
    with pytest.raises(TypeError):
        find_tallest_hero("Male", has_work)


def test_fetch_heroes_returns_non_empty_list(heroes):
    assert isinstance(heroes, list)
    assert len(heroes) > 0


def test_get_heroes_contains_expected_structure(heroes):
    hero = heroes[0]

    assert isinstance(hero, dict)
    assert "id" in hero
    assert "name" in hero
    assert "appearance" in hero
    assert "work" in hero


def test_api_is_available():
    response = requests.get(api_url, timeout=5)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_result_tallest_hero(heroes):
    result = find_tallest_hero("Male", True)
    result_height = height_cm(result)

    candidates = [
        hero
        for hero in heroes
        if hero.get("appearance", {}).get("gender") == "Male"
           and hero_has_work(hero) is True
           and height_cm(hero) is not None
    ]

    assert candidates
    assert result_height == max(height_cm(hero) for hero in candidates)