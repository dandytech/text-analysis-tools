from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from stockAnalyze import getCompanyStockInfo
from analyze import analyzedText
import json
import os

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
    analysis = analyzedText(data["text"])
    return jsonify(analysis)

# Main server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port
    app.run(host="0.0.0.0", port=port)