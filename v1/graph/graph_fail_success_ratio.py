import json
import matplotlib.pyplot as plt
import time

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

    bars = plt.bar(words_sorted, percentages_sorted, color='skyblue')
    plt.title('Failure Percentage in Last 100 Attempts')
    plt.xlabel('Word')
    plt.ylabel('Failure Percentage (%)')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 100)  # Limit the y-axis to 100% for clarity
    
    # Annotate bars with the total number of failures
    for bar, word in zip(bars, words_sorted):
        y_val = bar.get_height() 
        plt.text(bar.get_x() + bar.get_width()/2, y_val + 1, str(fail_counts[word]), ha='center', va='bottom')

    plt.tight_layout()
    plt.draw()
    plt.pause(0.5)
    plt.clf()

plt.figure(figsize=(12, 6))

while True:
    plot_fail_percentage()

