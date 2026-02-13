from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from stockAnalyze import getCompanyStockInfo
from analyze import analyzedText
import json

f = open('test/result.json')
stockDataTest = json.load(f)


app = Flask(__name__)
CORS(app)

@app.route('/health', methods=["GET"])
def health():
    return 'Health Check'

@app.route('/analyze-stock/<ticker>', methods=["GET"])
def analyzeStock(ticker):
    return stockDataTest
    # Validate ticker
    if len(ticker) > 5 or not ticker.isalpha():
        abort(400, description='Invalid ticker symbol')

    try:
        # Get analysis
        analysis = getCompanyStockInfo(ticker)
    except NameError as e:
        abort(404, e)
    except:
         abort(500, description='Something Went Wrong runing the stock analysis.')
    # ALWAYS return something
    return jsonify(analysis)

@app.route('/analyze-text', methods=["POST"])
def analyzeTextHandler():
    data = request.get_json()
    if "text" not in data or not data["text"]:
        abort(400, 'No Text provided to analyze.')
    analysis = analyzedText(data["text"])
    return analysis
   

# Main server
if __name__ == '__main__':
    app.run()