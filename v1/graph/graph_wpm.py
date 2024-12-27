import json
import matplotlib.pyplot as plt
import time

def plot_data():
    # 1. Read the JSON data from a file
    data = None
    try:
        with open('userdata.json', 'r') as f:   
            data = json.load(f)
    except:
        time.sleep(1.1)
        with open('userdata.json', 'r') as f:
            data = json.load(f)

    # 2. Extract and organize the data needed to plot the graph
    # Sort the sentence history by the number to ensure we have them in chronological order
    sentence_history = sorted(data['sentence_history'], key=lambda x: x['number'])

    sentence_numbers = [item['number'] for item in sentence_history]
    actual_wpm = [item['a_cpm']/5 for item in sentence_history]
    potential_wpm = [item['p_cpm']/5 for item in sentence_history]

    # 3. Use matplotlib to plot the graph
    plt.plot(sentence_numbers, actual_wpm, color='b', label='Actual WPM')
    plt.plot(sentence_numbers, potential_wpm, color='r', linestyle='--', label='Potential WPM')

    plt.fill_between(sentence_numbers, 0, actual_wpm, color='blue', alpha=0.2)  # Filling under Actual WPM
    plt.fill_between(sentence_numbers, actual_wpm, potential_wpm, color='red', alpha=0.2, label='Difference')  # Filling between Actual and Potential WPM
    
    plt.title('Actual vs Potential WPM over Time')
    plt.xlabel('Sentence Number')
    plt.ylabel('Words Per Minute (WPM)')
    plt.xticks(sentence_numbers)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.draw()
    plt.pause(1)
    plt.clf()

plt.figure(figsize=(10, 5))

while True:
    plot_data()
    time.sleep(0.5)

