from flask import Flask, abort, jsonify
from stockAnalyze import getCompanyStockInfo

app = Flask(__name__)

@app.route('/health')
def health():
    return 'Health Check'

@app.route('/analyze-stock/<ticker>')
def analyzeStock(ticker):
    # Validate ticker
    if len(ticker) > 5 or not ticker.isalpha():
        abort(400, description='Invalid ticker symbol')

    # Get analysis
    analysis = getCompanyStockInfo(ticker)

    # ALWAYS return something
    return jsonify(analysis)

# Main server
if __name__ == '__main__':
    app.run()