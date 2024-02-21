from flask import Flask, jsonify
from flask_cors import CORS
import client.texts
import json
import time
from collections import defaultdict, Counter

from analysis.find_weak_substrings import find_weak_substrings
from analysis.find_word_cpm_data import find_low_cpm_words, find_high_cpm_words

app = Flask(__name__)
CORS(app)

# Rolling average function
def rolling_average(data, window_size):
    cumsum = [0]
    result = []

    for i, x in enumerate(data, 1):
        cumsum.append(cumsum[i-1] + x)
        if i >= window_size:
            average = (cumsum[i] - cumsum[i-window_size]) / window_size
            result.append(average)

    return result

@app.route('/wpm-rolling-average', methods=['GET'])
def get_wpm_rolling_average():

    window_size = 50

    data = None
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    except:
        time.sleep(1.1)
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    
    sentence_history = data['sentence_history']
    
    actual_wpm = [entry['a_wpm'] for entry in sentence_history]
    potential_wpm = [entry['p_wpm'] for entry in sentence_history]
    typeracer_actual_wpm = [entry['a_cpm'] / 5 for entry in sentence_history]
    typeracer_potential_wpm = [entry['p_cpm'] / 5 for entry in sentence_history]

    result = jsonify({
        'a_wpm': rolling_average(reversed(typeracer_actual_wpm), window_size),
        'p_wpm': rolling_average(reversed(typeracer_potential_wpm), window_size),
    })

    print(result)
    
    return result

@app.route('/wpm', methods=['GET'])
def get_wpm():

    data = None

    try:
        with open('userdata.json', 'r') as f:   
            data = json.load(f)
    except FileNotFoundError:
        time.sleep(1.1)  # Consider handling the error differently
        with open('userdata.json', 'r') as f:
            data = json.load(f)

    sentence_history = sorted(data['sentence_history'], key=lambda x: x['number'])
    actual_wpm = [item['a_cpm']/5 for item in sentence_history]
    potential_wpm = [item['p_cpm']/5 for item in sentence_history]

    result = jsonify({
        'a_wpm': actual_wpm,
        'p_wpm': potential_wpm
    })

    print(result)

    return result

@app.route('/wpm-recent', methods=['GET'])
def get_wpm_recent():

    data = None

    try:
        with open('userdata.json', 'r') as f:   
            data = json.load(f)
    except FileNotFoundError:
        time.sleep(1.1)  # Consider handling the error differently
        with open('userdata.json', 'r') as f:
            data = json.load(f)

    sentence_history = sorted(data['sentence_history'], key=lambda x: x['number'])
    actual_wpm = [item['a_cpm']/5 for item in sentence_history]
    potential_wpm = [item['p_cpm']/5 for item in sentence_history]

    result = jsonify({
        'a_wpm': actual_wpm[-100:],
        'p_wpm': potential_wpm[-100:]
    })

    print(result)

    return result

@app.route('/word-pass-fail-ratio', methods=['GET'])
def plot_fail_percentage():
    # 1. Read the JSON data from a file
    data = None
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    except:
        time.sleep(1.1)
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    
    most_recent_attempt = data['sentence_history'][0]['number']
    window_start = most_recent_attempt - 100  # Only care about numbers within this window

    # 2 & 3. Count fails and successes for each word within the window
    fail_counts = {}
    for word, fails in data['fail_words'].items():
        fail_counts[word] = sum(1 for fail in fails if window_start <= fail['number'] <= most_recent_attempt)

    success_counts = {}
    for word, successes in data['success_words'].items():
        success_counts[word] = sum(1 for success in successes if window_start <= success['number'] <= most_recent_attempt)

    # Compute failure percentage
    fail_percentage = {}
    for word in fail_counts.keys():
        # ignore only one one zero fails
        if fail_counts[word] <= 1:
            continue
        total_attempts = fail_counts[word] + success_counts.get(word, 0)
        if total_attempts != 0:
            fail_percentage[word] = (fail_counts[word] / total_attempts) * 100
        else:
            fail_percentage[word] = 0

    # Plot the data, ordering by total number of failures per word
    words_sorted = sorted(fail_percentage.keys(), key=lambda x: fail_counts[x])  # Sort by ascending number of fails (for right-aligned highest fails)
    percentages_sorted = [fail_percentage[word] for word in words_sorted]

    returndata = []

    for word in words_sorted[-20:]:
        numfails = 0
        if word in fail_counts:
            numfails = fail_counts[word]
        
        numpass = 0
        if word in success_counts:
            numpass = success_counts[word]
        
        returndata.append({
            'word': word,
            'fails': numfails,
            'passes': numpass
        })

    result = jsonify(list(reversed(returndata)))

    return result

@app.route('/letter-error-rate', methods=['GET'])
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
    #recent_fail_words = [entry for entry in data['fail_words'].values() if entry[0]['number'] <= latest_attempt and entry[0]['number'] > latest_attempt - 100]
    
    recent_fail_words = []

    for word_fails in data['fail_words']:
        for fail in data['fail_words'][word_fails]:
            if fail['number'] > latest_attempt - 100:
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
        error_percentages[char] = (error_count / char_counter[char]) * 100

    # Sorting
    sorted_chars = sorted(error_counter, key=error_counter.get)
    sorted_errors = [error_counter[char] for char in sorted_chars]
    sorted_percentages = [error_percentages[char] for char in sorted_chars]
    
    return jsonify({
        "chars": sorted_chars,
        "errorcounts": sorted_errors,
        "percentages": sorted_percentages
    })

@app.route('/get-weak-substrings', methods=['GET'])
def get_weak_substrings():
    substrings = find_weak_substrings()

    substrs = []
    frequency = []

    for item in substrings:
        substrs.append(item["substring"])
        frequency.append(item["freq"])

    return jsonify({
        "substrings": substrs,
        "frequency": frequency
    })

@app.route('/get-low-cpm-words', methods=['GET'])
def get_low_cpm_words():
    low_cpm_words = find_low_cpm_words()
    return low_cpm_words

@app.route('/get-high-cpm-words', methods=['GET'])
def get_high_cpm_words():
    high_cpm_words = find_high_cpm_words()
    return high_cpm_words

if __name__ == '__main__':
    app.run(debug=True, port=44444)