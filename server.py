from flask import Flask

app = Flask(__name__)

@app.route('/health')
def hello_world():
    return 'Health Check'

@app.route('/analyze-stock')
def analyzeStock():
    return  {
        'data': 'Analysis coming soon'
    }

if __name__ == '__main__':
    app.run()