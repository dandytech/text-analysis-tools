from flask import Flask

app = Flask(__name__)

@app.route('/health')
def hello_world():
    return 'Health Check'

@app.route('/analyze-stock/<ticker>')
def analyzeStock(ticker):
    return  {
        'data': 'Analysis for ' + ticker + ' coming soon'
    }

if __name__ == '__main__':
    app.run()