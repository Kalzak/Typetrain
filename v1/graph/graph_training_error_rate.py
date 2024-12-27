import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def calculate_error_rate(data):
    recent_number = data["sentence_history"][0]["number"]
    relevant_errors = {word: [entry for entry in entries if entry["number"] > recent_number - 100] for word, entries in data["fail_words"].items()}

    error_rate = {}
    for word, entries in relevant_errors.items():
        success_entries = data["success_words"].get(word, [])
        success_count = len([entry for entry in success_entries if entry["number"] > recent_number - 100])
        total = len(entries) + success_count
        error_rate[word] = len(entries) / total if total != 0 else 0

    return error_rate

def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)

def update(frame):
    ax.clear()

    user_data = load_json("userdata.json")
    training_data = load_json("userdata.training.json")

    user_error_rate = calculate_error_rate(user_data)
    training_error_rate = calculate_error_rate(training_data)

    # Filter out words with more than 2 errors and get the top 50 highest error rates
    user_error_rate = {k: v for k, v in user_error_rate.items() if len(user_data["fail_words"][k]) > 2}
    sorted_words = sorted(user_error_rate, key=user_error_rate.get, reverse=True)[:50]

    user_rates = [user_error_rate[word] for word in sorted_words]
    training_rates = [training_error_rate.get(word, 0) for word in sorted_words]
    
    x = np.arange(len(sorted_words))
    width = 0.35  # Width of the bars

    bars1 = ax.bar(x - width/2, user_rates, width, label='User Data', color='b')
    bars2 = ax.bar(x + width/2, training_rates, width, label='Training Data', color='r')

    ax.set_title('Error Rate Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_words, rotation=90)
    ax.legend()

    # Annotate with the number of errors
    for word, bar1, bar2 in zip(sorted_words, bars1, bars2):
        user_errors = len(user_data["fail_words"].get(word, []))
        training_errors = len(training_data["fail_words"].get(word, []))
        
        ax.text(bar1.get_x() + bar1.get_width() / 2 - 0.15,
                bar1.get_height() + 0.005,
                str(user_errors),
                ha='center', color='black', fontsize=8)

        ax.text(bar2.get_x() + bar2.get_width() / 2 - 0.15,
                bar2.get_height() + 0.005,
                str(training_errors),
                ha='center', color='black', fontsize=8)

    plt.tight_layout()

    return bars1, bars2



fig, ax = plt.subplots(figsize=(10, 6))
ani = FuncAnimation(fig, update, repeat=True, interval=500)
plt.show()

