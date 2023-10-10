import json
import matplotlib.pyplot as plt
import time

def plot_mistyped_letters():
    # 1. Load the JSON data from the file
    data = None
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    except:
        with open('userdata.json', 'r') as f:
            data = json.load(f)

    # 2. Determine the number range for the last 100 attempts
    most_recent_attempt = data['sentence_history'][0]['number']
    window_start = most_recent_attempt - 100  # Only care about numbers within this window

    # 3. & 4. Iterate through each word in fail_words and count the frequency of each mistyped letter
    mistyped_counts = {}

    for word, fails in data['fail_words'].items():
        for fail in fails:
            if window_start <= fail['number'] <= most_recent_attempt:
                mistyped_letter = word[fail['index']]
                mistyped_counts[mistyped_letter] = mistyped_counts.get(mistyped_letter, 0) + 1

    # 5. Plot the results in a bar chart
    letters_sorted = sorted(mistyped_counts.keys(), key=lambda x: mistyped_counts[x])  # Sort by number of mistakes
    counts_sorted = [mistyped_counts[letter] for letter in letters_sorted]

    bars = plt.bar(letters_sorted, counts_sorted, color='coral')
    plt.title('Mistyped Letters in Last 100 Attempts')
    plt.xlabel('Letter')
    plt.ylabel('Mistyped Count')
    plt.xticks(rotation=45)
    
    for bar in bars:
        y_val = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, y_val + 0.5, str(int(y_val)), ha='center', va='bottom')

    plt.tight_layout()
    plt.draw()
    plt.pause(0.5)
    plt.clf()

plt.figure(figsize=(10, 5))

while True:
    plot_mistyped_letters()

