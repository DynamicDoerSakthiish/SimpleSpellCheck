import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from spellchecker import SpellChecker
import pytest
import os

def find_misspelled_words_locations(misspelled, elements):
    misspelled_locations = []
    for word in misspelled:
        for idx, element in enumerate(elements):
            if word in element.text:
                misspelled_locations.append((word, idx, element.text))
                break
    return misspelled_locations

def find_incorrect_capitalization_locations(elements):
    incorrect_capitalization_locations = []
    for idx, element in enumerate(elements):
        if not has_correct_capitalization(element.text):
            incorrect_capitalization_locations.append((idx, element.text))
    return incorrect_capitalization_locations

def write_errors_to_file(errors, filename):
    with open(filename, 'w') as f:
        for error in errors:
            f.write(str(error) + '\n')

def test_spelling_and_capitalization(driver, url):
    driver.get(url)

    # Adjust the selector to target the elements containing text on your webpage
    elements = driver.find_elements(By.CSS_SELECTOR, "body *")

    text = extract_text_from_elements(elements)

    spell = SpellChecker()
    words = re.findall(r'\b\w+\b', text)
    misspelled = spell.unknown(words)

    misspelled_locations = find_misspelled_words_locations(misspelled, elements)
    incorrect_capitalization_locations = find_incorrect_capitalization_locations(elements)

    errors = {
        'url': url,
        'misspelled': misspelled_locations,
        'incorrect_capitalization': incorrect_capitalization_locations
    }

def test_spelling_and_capitalization(driver, url):
    driver.get(url)

    # Adjust the selector to target the elements containing text on your webpage
    elements = driver.find_elements(By.CSS_SELECTOR, "body *")
    text = extract_text_from_elements(elements)

    # Display the tag name and text of each element
    for element in elements:
        print(f"Tag: {element.tag_name}, Text: {element.text}")

    spell = SpellChecker()
    words = re.findall(r'\b\w+\b', text)
    misspelled = spell.unknown(words)

    assert len(misspelled) == 0, f"Misspelled words: {misspelled}"

    assert has_correct_capitalization(text), "Incorrect capitalization found"

    output_file = os.path.join('errors', f"errors_{url.split('/')[-1]}.txt")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    write_errors_to_file(errors, output_file)

    assert len(misspelled) == 0, f"Misspelled words: {misspelled}"

    assert has_correct_capitalization(text), "Incorrect capitalization found"

def extract_text_from_elements(elements):
    return ' '.join([element.text for element in elements])

def has_correct_capitalization(text):
    words = re.findall(r'\b\w+\b', text)
    for word in words:
        if word.islower() or word.isupper():
            continue
        if not word[0].isupper():
            return False
    return True

@pytest.fixture(scope="module")
def driver():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

@pytest.mark.parametrize("url", [
    "https://www.doerscircle.com/solutions?_gl=1*1ew4o89*_ga*MzExMzM1NzEzLjE2Nzc2MzI3MTI.*_ga_7T8T71LXL9*MTY3ODg3MTU3NS4yMC4xLjE2Nzg4NzQzOTAuMC4wLjA.",
    "https://sit.doerscircle.com/solutions/incorporation",
    "https://sit.doerscircle.com/solutions/incorporation-foreigner-freelancer",
    "https://sit.doerscircle.com/solutions/incorporation-foreigner-sme",
    "https://sit.doerscircle.com/solutions/thai-incorporation",
    "https://sit.doerscircle.com/solutions/registered-business-address",
    "https://sit.doerscircle.com/solutions/corporate-advisory",
    "https://sit.doerscircle.com/account/profile",
    "https://www.doerscircle.com/benefits",
    "https://www.doerscircle.com/about",
    "https://www.doerscircle.com/freelance",
    "https://www.doerscircle.com/freelance-th",
    "https://www.doerscircle.com/membership",
    "https://www.doerscircle.com/enterprise",
    "https://app.doerscircle.com/solutions/premium-membership",
    # Add more URLs if needed
])
def test_spelling_and_capitalization(driver, url):
    driver.get(url)

    # Adjust the selector to target the elements containing text on your webpage
    elements = driver.find_elements(By.CSS_SELECTOR, "body *")
    text = extract_text_from_elements(elements)

    spell = SpellChecker()
    words = re.findall(r'\b\w+\b', text)
    misspelled = spell.unknown(words)

    assert len(misspelled) == 0, f"Misspelled words: {misspelled}"

    assert has_correct_capitalization(text), "Incorrect capitalization found"

#pytest spell_Check.py
