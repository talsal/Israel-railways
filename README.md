to run the test:
pytest israelRailWays.py from terminal on the directory that you have the code


In in this task i will demonstrate API interaction, automation testing with Selenium WebDriver and Python on the Rick and Morty API + Google site using Selenium 

API section
base URL: Rick and Morty API.
Fetching all episodes using the 'base_url'.
Randomly choosing one episode from the list where the number of characters exceeds or equals 30.
Printing the name of the selected episode and the number of characters in it.
Randomly selecting two characters from the chosen episode and store them as Character objects
For each character, i write a friendly introduction to a text file named
characters_introduction.txt: Format: "Hi! I'm CHARACTER_NAME, My ID is CHARACTER_ID, I'm from LOCATION_NAME, etc."

UI Automation (Selenium)
Opening Chrome Browser, window is maximized, Navigating to Google.com, and use English as the browser's language.
Navigate to Google Images:
Searching for the First Character, Search for 'Rick and Morty FIRST_CHARACTER_NAME'.
Click on the Correct Image, Using the first character's ID, calculate the correct image position using the hundreds/tens digit plus the ones digit. (e.g. ID = 123 => position = 1+3)
If the character’sID has fewer than 3 digits, use the tens and ones digits for grid calculation.
Capture the selected image in a screenshot and save it as FIRST_CHARACTER_NAME- ID-TIMESTAMP.jpg.
The TIMESTAMP will be human-readable, containing the screenshot's date and time.
Navigate to the Second Character's Image:
Retrieve the URL of the second character’s image and repeat the screenshot process. o Bonus: Capture only the specific image without background elements.
Close the Browser.

Verification and Assertion section:
Verify that the locations of the two selected characters are the same – using Python assert
Assertions: 
If the locations differ, print:
"FIRST_CHARACTER_NAME from FIRST_CHARACTER_LOCATION and SECOND_CHARACTER_NAME from SECOND_CHARACTER_LOCATION."
If the locations match, print:
"Both characters are from LOCATION_NAME."
      
