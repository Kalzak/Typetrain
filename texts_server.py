from flask import Flask, jsonify
from flask_cors import CORS
import client.texts

app = Flask(__name__)
CORS(app)

@app.route('/get-text', methods=['GET'])
def get_text():
    # Here, you make calls to another website to load the texts
    # For example, using requests.get('https://example.com')
    # Assuming you store the text in a variable named 'text'
    text = client.texts.get_typeracer_text()
    
    # Return the text in JSON format
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)