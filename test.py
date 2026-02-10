import random
from flask import Flask, jsonify

app = Flask(__name__)

quotes = [
    {"text": "An eye for an eye.", "title": "Mahatma Gandhi"},
    {"text": "When in doubt, tell the truth.", "title": "Mark Twain"},
    {"text": "You are who you choose to be.", "title": "Mark Twain"},
]

@app.route('/quotes/random', methods=['GET'])
def get_random_quotes():
    return jsonify(random.choice(quotes))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
