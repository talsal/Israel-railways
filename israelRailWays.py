from time import sleep

import pytest
from PIL import Image
import requests
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime


# utils function
def calculate_image_position(character_id):
    """Calculates the image position based on the character ID."""
    if character_id < 100:
        return character_id // 10 + character_id % 10
    else:
        return (character_id // 100) + (character_id % 10)

def get_random_episode_with_many_characters(cur_base_url):
    """Fetches all episodes, selects a random one with >= 30 characters, and returns it."""
    response = requests.get(cur_base_url + "/episode")
    episodes = json.loads(response.text)["results"]

    episodes_with_many_characters = [cur_episode for cur_episode in episodes if len(cur_episode["characters"]) >= 30]
    return random.choice(episodes_with_many_characters)

def get_characters(cur_base_url, cur_character_ids):
    """Fetches multiple characters simultaneously using a single API call."""
    character_ids_str = ",".join(str(cur_id) for cur_id in cur_character_ids)
    response = requests.get(cur_base_url + "/character/" + character_ids_str)
    return json.loads(response.text)

def write_character_introductions(cur_characters, cur_filename):
    """Writes friendly introductions for each character to a text file."""
    with open(cur_filename, "w") as f:
        for character in cur_characters:
            f.write(f"Hi! I'm {character['name']}, My ID is {character['id']}, I'm from {character['location']['name']}, etc.\n")

def get_character_ids(character_urls):
    """Extracts character IDs from a list of character URLs."""
    cur_character_ids = []
    for character_url in character_urls:
        # Extract the ID from the URL (assuming a specific URL format)
        character_id = int(character_url.split("/")[-1])
        cur_character_ids.append(character_id)
    return cur_character_ids


# task 1 - API
base_url = "https://rickandmortyapi.com/api"

# Get a random episode with many characters
episode = get_random_episode_with_many_characters(base_url)
print(f"Selected episode: {episode['name']} ({episode['characters']} characters)")

# Randomly select two characters from the episode
character_ids_urls = random.sample(episode["characters"], 2)
character_ids = get_character_ids(character_ids_urls)

# Fetch both characters simultaneously
characters = get_characters(base_url, character_ids)

# Write character introductions to a file
write_character_introductions(characters, "characters_introduction.txt")

# this will create the webdriver just once for all the module - this file
# it will close the driver after all tests finished
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
    verify()

@pytest.mark.parametrize("character", characters)
def test_ui(driver,character):
    navigate_google_images(driver)
    search_character(driver, character)
    select_image_and_take_screenshot(driver, character)


def navigate_google_images(driver):
    # step 2
    # navigate to google page --> eng --> images
    driver.get("https://www.google.com/search?hl=en")
    images_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//*[@id='gb']/div/div[1]/div/div[2]/a"))
    )
    images_button.click()

def search_character(driver,character):
    # step 3
    # search for character
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"Rick and Morty Character {character['name']}")
    search_box.send_keys(Keys.ENTER)
    sleep(1)

def select_image_and_take_screenshot(driver,character):
    # step 4
    """Selects the correct image based on its position."""
    image_position = calculate_image_position(character['id'])
    image_element = driver.find_element(By.XPATH, "//div[@id='rso']/div/div/div/div/div[1]/div[" + str(image_position) + "]")
    image_element.click()
    sleep(5)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = "character_" + character['name']
    filepath = f"{filename}-{now}.jpg"
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")

    # Get the location and dimensions of the image element
    location = image_element.location
    size = image_element.size

    # Crop the image
    image = Image.open(filepath)
    cropped_image = image.crop(
        (location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']))
    cropped_image.save(filepath,'JPEG')

def verify():
    # Task 3 - Verification and Assertion
    first_character_location = characters[0]["location"]["name"]
    second_character_location = characters[1]["location"]["name"]

    # Assertion: Verify locations
    assert first_character_location == second_character_location, f"""
    Locations differ!
    {characters[0]['name']} from {first_character_location} and {characters[1]['name']} from {second_character_location}.
    """

    print(f"Both characters are from {first_character_location}.")




