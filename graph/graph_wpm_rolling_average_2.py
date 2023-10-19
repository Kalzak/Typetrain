import json
import matplotlib.pyplot as plt
from collections import deque
import time

# Rolling average function
def rolling_average(data, window_size):
    cumsum = [0]
    for i, x in enumerate(data, 1):
        cumsum.append(cumsum[i-1] + x)
        if i >= window_size:
            average = (cumsum[i] - cumsum[i-window_size]) / window_size
            yield average

def get_wpm_data():
    data = None
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    except:
        time.sleep(0.1)
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    
    sentence_history = data['sentence_history']
    
    actual_wpm = [entry['a_wpm'] for entry in sentence_history]
    potential_wpm = [entry['p_wpm'] for entry in sentence_history]
    typeracer_actual_wpm = [entry['a_cpm'] / 5 for entry in sentence_history]
    typeracer_potential_wpm = [entry['p_cpm'] / 5 for entry in sentence_history]

    return list(reversed(actual_wpm)), list(reversed(potential_wpm)), list(reversed(typeracer_actual_wpm)), list(reversed(typeracer_potential_wpm))

fig, ax = plt.subplots(figsize=(12, 6))

while True:
    actual_wpm, potential_wpm, typeracer_actual_wpm, typeracer_potential_wpm = get_wpm_data()

    # Get the rolling average for the data
    rolling_actual_wpm = list(rolling_average(actual_wpm, 10))
    rolling_potential_wpm = list(rolling_average(potential_wpm, 10))
    rolling_typeracer_actual_wpm = list(rolling_average(typeracer_actual_wpm, 10))
    rolling_typeracer_potential_wpm = list(rolling_average(typeracer_potential_wpm, 10))
    
    x = list(range(9, len(actual_wpm)))

    ax.clear()

    ax.plot(x, rolling_actual_wpm, color="green", label="Actual WPM (Native)", linewidth=1.5)
    ax.plot(x, rolling_potential_wpm, color="green", linestyle="--", label="Potential WPM (Native)", linewidth=1.5)
    ax.plot(x, rolling_typeracer_actual_wpm, color="orange", label="Actual WPM (TypeRacer)", linewidth=1.5)
    ax.plot(x, rolling_typeracer_potential_wpm, color="orange", linestyle="--", label="Potential WPM (TypeRacer)", linewidth=1.5)

    ax.set_title("Rolling Average of Actual vs Potential WPM", fontsize=16)
    ax.set_xlabel("Attempt Number", fontsize=14)
    ax.set_ylabel("WPM", fontsize=14)
    ax.legend(loc='lower left', fontsize=11)
    
    # Adding grid lines and adjusting y-axis
    ax.yaxis.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.set_yticks(range(0, int(max(rolling_potential_wpm)+10), 5))

    plt.draw()
    plt.pause(0.5)

