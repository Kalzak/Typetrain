from flask import Flask, jsonify
from flask_cors import CORS
import client.texts
import json

app = Flask(__name__)
CORS(app)

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