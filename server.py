from flask import Flask, abort

app = Flask(__name__)

@app.route('/health')
def hello_world():
    return 'Health Check'

@app.route('/analyze-stock/<ticker>')
def analyzeStock(ticker):
    if len(ticker) > 5 or not ticker.isidentifier():
        abort(400, 'Invalid ticker symbol')
        return {'data': 'Analysis for ' + ticker + ' coming soon'}
    
# The main server function
if __name__ == '__main__':
    app.run()