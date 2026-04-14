from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from stockAnalyze import getCompanyStockInfo
from analyze import analyzedText
import json
import os

# Ensure result folder exists for WordClouds
os.makedirs("result", exist_ok=True)

# Load test data
with open('test/result.json') as f:
    stockDataTest = json.load(f)

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=["GET"])
def health():
    return 'Flask Server is Running'

@app.route('/analyze-stock/<ticker>', methods=["GET"])
def analyzeStock(ticker):
    # return stockDataTest  # uncomment to use test data

    # Validate ticker
    if len(ticker) > 5 or not ticker.isalpha():
        abort(400, description='Invalid ticker symbol')
    try:
        analysis = getCompanyStockInfo(ticker)
    except NameError as e:
        abort(404, str(e))
    except Exception as e:
        print(f"Error running the stock analysis: {e}")
        abort(500, description='Something went wrong running the stock analysis.')
    return jsonify(analysis)

@app.route('/analyze-text', methods=["POST"])
def analyzeTextHandler():
    data = request.get_json()
    if "text" not in data or not data["text"]:
        abort(400, 'No text provided to analyze.')
    try:
        analysis = analyzedText(data["text"])
    except Exception as e:
        print(f"Error running text analysis: {e}")
        abort(500, description='Text analysis failed.')
    return jsonify(analysis)

# Main server
if __name__ == '__main__':
    # Render assigns a PORT via environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)