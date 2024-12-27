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
    
    return sorted_chars, sorted_errors, sorted_percentages

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

while True:
    sorted_chars, sorted_errors, sorted_percentages = get_mistyped_data()

    ax1.clear()
    ax2.clear()

    bars = ax1.bar(sorted_chars, sorted_errors, color='gray', label='Total Errors')
    line, = ax2.plot(sorted_chars, sorted_percentages, color='red', marker='o', linestyle='dashed', label='Error Percentage')

    # Annotate bar chart
    for bar in bars:
        height = bar.get_height()
        ax1.annotate('{}'.format(height),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom')

    # Annotate line chart
    for xi, yi in zip(range(len(sorted_chars)), sorted_percentages):
        ax2.annotate(f"{yi:.2f}%", (xi, yi), textcoords="offset points", xytext=(0,5), ha='center', color='red')

    ax1.set_xlabel('Character')
    ax1.set_ylabel('Total Errors', color='gray')
    ax2.set_ylabel('Error Percentage (%)', color='red')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title('Mistyped Characters in the Last 100 Attempts')
    plt.draw()
    plt.pause(0.5)
