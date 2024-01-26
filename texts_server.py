from flask import Flask, jsonify
from flask_cors import CORS
import client.texts
import stats_server
import json
import time
from collections import defaultdict, Counter

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route('/get-text', methods=['GET'])
def get_text():
    # Here, you make calls to another website to load the texts
    # For example, using requests.get('https://example.com')
    # Assuming you store the text in a variable named 'text'
    text = client.texts.get_typeracer_text()
    
    # Return the text in JSON format
    return jsonify({'text': text})

@app.route('/get-weak-substrings', methods=['GET'])
def get_weak_substrings():
    text = client.texts.get_weak_substrings()
    return jsonify({'text': text})

@app.route('/get-weak-substring-words', methods=['GET'])
def get_weak_substring_words():
    text = client.texts.get_weak_substring_words()
    return jsonify({'text': text})

@app.route('/get-llm-text', methods=['GET'])
def get_llm_text():
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

    text = client.texts.generate_text_openai(words_sorted[-30:])
    return jsonify({'text': text})


if __name__ == '__main__':
    app.run(debug=True)