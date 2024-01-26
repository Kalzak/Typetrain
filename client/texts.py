import os
from openai import OpenAI
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import sys

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(script_dir, '..', 'analysis')))

from find_weak_substrings import find_weak_substrings
from find_weak_substring_words import find_weak_substring_words

# Simple texts for quick testing
simple_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "A watched pot never boils.",
    "All that glitters is not gold.",
    "Actions speak louder than words.",
    "Where there's a will, there's a way.",
    "Every cloud has a silver lining.",
    "Don't count your chickens before they hatch.",
    "Birds of a feather flock together.",
    "A penny for your thoughts.",
    "You can't judge a book by its cover."
]

# A set of ranges for typeracer text ids
typeracer_text_id_ranges = [
    [1, 790],
    [3100000, 3100109],
    [3550000, 3550118],
    [3550232, 3550486],
    [3550488, 3550657],
    [3810820, 3810940],
    [3811367, 3811468],
    [4060176, 4060291],
    [4070000, 4070207],
    [4070209, 4070315],
    [4180218, 4180863],
    [4350053, 4350700],
    [4940000, 4940217],
    [5390000, 5390489],
]


# Returns a simple text for testing
def get_simple_text():
    return random.choice(simple_texts)


# Returns a random typeracer text
def get_typeracer_text():
    text_id_range = random.choice(typeracer_text_id_ranges)
    text_id = random.randint(text_id_range[0], text_id_range[1])

    # TODO create folder if not exists rather than expect exists
    url = f"https://typeracerdata.com/text?id={text_id}"
    path = f"texts/{text_id}.txt"
    if not os.path.exists(path):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text_element = soup.find("p")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as file:
                file.write(text_element.text[2:])
            return text_element.text[2:]
    else:
        with open(path, "r") as file:
            return file.readline()

def get_cached_typeracer_text():
    texts = os.listdir("texts/")
    text_file = random.choice(texts)
    file_contents = ""
    with open(f"texts/{text_file}", 'r') as file:
        file_contents = file.read()
    return file_contents

# Creates a text by randomly placing provided words
def generate_text_words(wordlist):
    paragraph = []
    while len(paragraph) < 30:
        random_string = random.choice(wordlist)
        paragraph.append(random_string)
    return ' '.join(paragraph)


# Uses ChatGPT to generate a text containing provided words
def generate_text_openai(words):

    # Load the env every time, not efficient but whatever
    load_dotenv()
    
    words_string = "\n - ".join(words)
    request_string = "I am doing typing training, please write a paragraph using these words. Just reply with the paragraph only please. Try and have between 20-50 words please." + words_string

    client = OpenAI(
        api_key = os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": request_string
            }
        ],
        temperature=1.4,
        model="gpt-3.5-turbo"
    )

    return chat_completion.choices[0].message.content

def get_weak_substrings():
    substrings = find_weak_substrings()
    total_freq = sum(substring['freq'] for substring in substrings)

    paragraph = []

    for _ in range(40):
        rand_val = random.randint(1, total_freq)
        cumulative_freq = 0

        for substring in substrings:
            cumulative_freq += substring['freq']
            if rand_val <= cumulative_freq:
                paragraph.append(substring['substring'].replace(" ", "."))
                break

    return ' '.join(paragraph)

def get_weak_substring_words():
    weak_substring_words = find_weak_substring_words(5, 40)
    return ' '.join(weak_substring_words)


