import json
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import time

def get_mistyped_data():
    # Load the JSON data
    data = None
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    except:
        time.sleep(1.1)
        with open('userdata.json', 'r') as f:
            data = json.load(f)
        
    latest_attempt = data['sentence_history'][0]['number']
    recent_fail_words = []

    for word_fails in data['fail_words']:
        for fail in data['fail_words'][word_fails]:
            #if fail['number'] > latest_attempt - 100:
            if 1 == 1:
                recent_fail_words.append(fail)

    lowest_number = 1000

    # Count the errors for each letter
    error_counter = defaultdict(int)
    for entry in recent_fail_words:
        error_char = entry['word'][entry['index']]

        if entry['number'] < lowest_number:
            lowest_number = entry['number']
            
        error_counter[error_char.lower()] += 1

    # Count total occurrences of each character in the last 100 sentences
    char_counter = Counter("".join([entry['sentence'] for entry in data['sentence_history'] if entry['number'] <= latest_attempt and entry['number'] > latest_attempt - 100]))

    # Calculate the percentage error for each character
    error_percentages = {}
    for char, error_count in error_counter.items():
        print(char * error_count, end="")

if __name__ == "__main__":
    get_mistyped_data()
    print("\n\nAlright cool you can copy/paste those letters here to get a heatmap: https://www.patrick-wied.at/projects/heatmap-keyboard/")