import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def calculate_avg_cpm(data):
    avg_cpm = {}
    for word, stats in data['success_words'].items():
        cpms = [entry['cpm'] for entry in stats]  # extracting cpm values from dictionaries
        avg_cpm[word] = sum(cpms) / len(cpms)
    return avg_cpm

def update(frame):
    plt.clf()  # Clear the current plot

    # Load the data from the files
    with open('userdata.json', 'r') as f:
        user_data = json.load(f)

    with open('userdata.training.json', 'r') as f:
        training_data = json.load(f)

    # Calculate the average CPM for each word in userdata.json
    user_avg_cpm = calculate_avg_cpm(user_data)

    # Sort words by CPM and select the 50 lowest CPM words
    sorted_words = sorted(user_avg_cpm, key=user_avg_cpm.get)[:50]

    # Fetch the average CPM for each of these words from userdata.training.json
    training_avg_cpm = calculate_avg_cpm(training_data)
    comparison_data = [(word, user_avg_cpm[word], training_avg_cpm.get(word, None)) for word in sorted_words if word in training_avg_cpm]

    # Plot
    words, user_cpms, training_cpms = zip(*comparison_data)

    bar_width = 0.35
    index = np.arange(len(words))

    bar1 = plt.bar(index, user_cpms, bar_width, color='b', label='Original CPM')
    bar2 = plt.bar(index + bar_width, training_cpms, bar_width, color='g', label='Training CPM')

    plt.xlabel('Words')
    plt.ylabel('CPM')
    plt.title('CPM Comparison between Original and Training Data for 50 Lowest CPM Words')
    plt.xticks(index + bar_width / 2, words, rotation=90)
    plt.legend()
    plt.tight_layout()

fig = plt.figure(figsize=(15, 8))
ani = FuncAnimation(fig, update, interval=500)  # 500ms = 0.5 seconds
plt.show()
