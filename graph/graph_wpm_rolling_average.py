import json
import matplotlib.pyplot as plt
import time

def rolling_average(values, window):
    """Compute rolling average with a given window size."""
    return [sum(values[i:i+window])/window for i in range(len(values) - window + 1)]

def plot_wpm():
    # Load the JSON data
    data = None
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    except:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
        
    sentence_history = sorted(data['sentence_history'], key=lambda x: x['number'])

    actual_wpm = [entry['a_wpm'] for entry in sentence_history]
    potential_wpm = [entry['p_wpm'] for entry in sentence_history]

    # Compute rolling averages
    rolling_window = 10
    smoothed_actual = rolling_average(actual_wpm, rolling_window)
    smoothed_potential = rolling_average(potential_wpm, rolling_window)

    x_values = list(range(rolling_window-1, len(actual_wpm)))  # Start from the 9th entry (0-indexed)

    plt.fill_between(x_values, smoothed_actual, color='grey', alpha=0.5)
    plt.fill_between(x_values, smoothed_actual, smoothed_potential, color='lightgrey', alpha=0.5)
    plt.plot(x_values, smoothed_actual, label='Actual WPM', color='black')
    plt.plot(x_values, smoothed_potential, label='Potential WPM', color='red', linestyle='dashed')
    
    plt.legend()
    plt.xlabel("Sentence Number")
    plt.ylabel("Words Per Minute (WPM)")
    plt.title("Rolling Average of WPM Over Time")

    plt.draw()
    plt.pause(0.5)
    plt.clf()

plt.figure(figsize=(10, 5))

while True:
    plot_wpm()

