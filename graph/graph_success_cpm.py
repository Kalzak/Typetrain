import json
import matplotlib.pyplot as plt
import time

def plot_avg_cpm():
    # 1. Read the JSON data from a file
    data = None
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    except:
        time.sleep(1.1)
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    
    # 2. Extract and organize the data needed to compute average CPM for each word
    words = []
    avg_cpms = []
    for word, attempts in data['success_words'].items():
        cpms = [attempt['cpm'] for attempt in attempts[-100:]]  # Take the last 100 attempts, or less if not available
        avg_cpm = sum(cpms) / len(cpms) if cpms else 0  # Calculate average CPM
        words.append(word)
        avg_cpms.append(avg_cpm)

    # Sorting data by average CPM
    sorted_indices = sorted(range(len(avg_cpms)), key=lambda k: avg_cpms[k])
    words = [words[i] for i in sorted_indices]
    avg_cpms = [avg_cpms[i] for i in sorted_indices]

    words = words[0:30] + words[-30:]
    avg_cpms = avg_cpms[0:30] + avg_cpms[-30:]

    # 3. Use matplotlib to plot the graph as a line chart
    plt.plot(words, avg_cpms, marker='o', color='skyblue', linestyle='-')
    plt.title('Average CPM for Last 100 Attempts (or less) per Word')
    plt.xlabel('Word')
    plt.ylabel('Average Characters Per Minute (CPM)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.draw()
    plt.pause(0.5)
    plt.clf()

plt.figure(figsize=(12, 6))

while True:
    plot_avg_cpm()

