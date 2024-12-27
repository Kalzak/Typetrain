import time
import json

def load_data(filepath):
    data = None
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except:
        time.sleep(1.1)
        with open(filepath, 'r') as f:
            data = json.load(f)
    return data

def find_low_cpm_words():
    userdata = load_data('userdata.json')
    words = userdata["success_words"]

    worddata = {}

    for word in words:
        total_attempts = len(words[word])
        cpm_sum = 0
        if total_attempts > 1 and len(word) > 2 and not "\"" in word and word[0] != "'" and word[-1] != "'" and not "(" in word and not "(" in word:
            for attempt in words[word]:
                cpm_sum += attempt["cpm"]
            worddata[word] = cpm_sum/total_attempts
    
    sorted_worddata = dict(sorted(worddata.items(), key=lambda x: x[1]))
    bottom_25_percent = dict(list(sorted_worddata.items())[:int(len(sorted_worddata) * 0.25)])

    print(bottom_25_percent)

    return bottom_25_percent

def find_high_cpm_words():
    userdata = load_data('userdata.json')
    words = userdata["success_words"]

    worddata = {}

    for word in words:
        total_attempts = len(words[word])
        cpm_sum = 0
        if total_attempts > 1 and len(word) > 2 and not "\"" in word and word[0] != "'" and word[-1] != "'" and not "(" in word and not "(" in word:
            for attempt in words[word]:
                cpm_sum += attempt["cpm"]
            worddata[word] = cpm_sum/total_attempts
    
    sorted_worddata = dict(sorted(worddata.items(), key=lambda x: x[1], reverse=True))
    top_25_percent = dict(list(sorted_worddata.items())[:int(len(sorted_worddata) * 0.25)])
    
    print(top_25_percent)

    return top_25_percent