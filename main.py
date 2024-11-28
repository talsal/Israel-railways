from time import sleep
from PIL import Image
import requests
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime



# task 1 api functions
def get_random_episode_with_many_characters(base_url):
    """Fetches all episodes, selects a random one with >= 30 characters, and returns it."""
    response = requests.get(base_url + "/episode")
    episodes = json.loads(response.text)["results"]

    episodes_with_many_characters = [episode for episode in episodes if len(episode["characters"]) >= 30]
    return random.choice(episodes_with_many_characters)

def get_characters(base_url, character_ids):
    """Fetches multiple characters simultaneously using a single API call."""
    character_ids_str = ",".join(str(id) for id in character_ids)
    response = requests.get(base_url + "/character/" + character_ids_str)
    return json.loads(response.text)

def write_character_introductions(characters, filename):
    """Writes friendly introductions for each character to a text file."""
    with open(filename, "w") as f:
        for character in characters:
            f.write(f"Hi! I'm {character['name']}, My ID is {character['id']}, I'm from {character['location']['name']}, etc.\n")

def get_character_ids(character_urls):
    """Extracts character IDs from a list of character URLs."""
    character_ids = []
    for character_url in character_urls:
        # Extract the ID from the URL (assuming a specific URL format)
        character_id = int(character_url.split("/")[-1])
        character_ids.append(character_id)
    return character_ids


# task 2 ui functions

def navigate_to_google_images(driver):
    images_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='gb']/div/div[1]/div/div[2]/a"))
    )
    images_button.click()

def take_screenshot(driver, filename, image_element):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
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


def calculate_image_position(character_id):
    """Calculates the image position based on the character ID."""
    if character_id < 100:
        return character_id // 10 + character_id % 10
    else:
        return (character_id // 100) + (character_id % 10)


def character_image_location(character):

    # step 1
    driver = webdriver.Chrome()
    driver.maximize_window()

    # step 2
    # navigate to google page --> eng --> images
    driver.get("https://www.google.com/search?hl=en")
    navigate_to_google_images(driver)

    # step 3
    # search for character
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"Rick and Morty Character {character['name']}")
    search_box.send_keys(Keys.ENTER)
    sleep(1)

    # step 4
    """Selects the correct image based on its position."""
    image_position = calculate_image_position(character['id'])
    image_element = driver.find_element(By.XPATH, "//div[@id='rso']/div/div/div/div/div[1]/div[" + str(image_position) + "]")
    image_element.click()
    sleep(5)

    # step 5
    take_screenshot(driver, f"character_{character['name']}", image_element)
    driver.quit()


def main():

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

    # task 2 - UI selenium
    for character in characters:
        character_image_location(character)

    # Task 3 - Verification and Assertion
    first_character_location = characters[0]["location"]["name"]
    second_character_location = characters[1]["location"]["name"]

    # Assertion: Verify locations
    assert first_character_location == second_character_location, f"""
    Locations differ!
    {characters[0]['name']} from {first_character_location} and {characters[1]['name']} from {second_character_location}.
    """

    print(f"Both characters are from {first_character_location}.")


if __name__ == "__main__":
    main()

