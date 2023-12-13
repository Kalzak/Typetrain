from flask import Flask, jsonify
from flask_cors import CORS
import client.texts
import json

app = Flask(__name__)
CORS(app)

# Rolling average function
def rolling_average(data, window_size):
    cumsum = [0]
    result = []

    for i, x in enumerate(data, 1):
        cumsum.append(cumsum[i-1] + x)
        if i >= window_size:
            average = (cumsum[i] - cumsum[i-window_size]) / window_size
            result.append(average)

    return result

@app.route('/wpm-rolling-average', methods=['GET'])
def get_wpm_rolling_average():

    window_size = 50

    data = None
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    except:
        time.sleep(1.1)
        with open('userdata.json', 'r') as f:
            data = json.load(f)
    
    sentence_history = data['sentence_history']
    
    actual_wpm = [entry['a_wpm'] for entry in sentence_history]
    potential_wpm = [entry['p_wpm'] for entry in sentence_history]
    typeracer_actual_wpm = [entry['a_cpm'] / 5 for entry in sentence_history]
    typeracer_potential_wpm = [entry['p_cpm'] / 5 for entry in sentence_history]

    result = jsonify({
        'a_wpm': rolling_average(reversed(typeracer_actual_wpm), window_size),
        'p_wpm': rolling_average(reversed(typeracer_potential_wpm), window_size),
    })

    print(result)
    
    return result

@app.route('/wpm', methods=['GET'])
def get_wpm():

    data = None

    try:
        with open('userdata.json', 'r') as f:   
            data = json.load(f)
    except FileNotFoundError:
        time.sleep(1.1)  # Consider handling the error differently
        with open('userdata.json', 'r') as f:
            data = json.load(f)

    sentence_history = sorted(data['sentence_history'], key=lambda x: x['number'])
    actual_wpm = [item['a_cpm']/5 for item in sentence_history]
    potential_wpm = [item['p_cpm']/5 for item in sentence_history]

    result = jsonify({
        'a_wpm': actual_wpm,
        'p_wpm': potential_wpm
    })

    print(result)

    return result

@app.route('/wpm-recent', methods=['GET'])
def get_wpm_recent():

    data = None

    try:
        with open('userdata.json', 'r') as f:   
            data = json.load(f)
    except FileNotFoundError:
        time.sleep(1.1)  # Consider handling the error differently
        with open('userdata.json', 'r') as f:
            data = json.load(f)

    sentence_history = sorted(data['sentence_history'], key=lambda x: x['number'])
    actual_wpm = [item['a_cpm']/5 for item in sentence_history]
    potential_wpm = [item['p_cpm']/5 for item in sentence_history]

    result = jsonify({
        'a_wpm': actual_wpm[-100:],
        'p_wpm': potential_wpm[-100:]
    })

    print(result)

    return result



if __name__ == '__main__':
    app.run(debug=True, port=44444)