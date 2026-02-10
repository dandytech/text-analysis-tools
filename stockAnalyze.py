import json
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import analyze  

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/119.0.0.0 Safari/537.36'
    )
}

# ---------------- BASIC INFO ----------------
def extractBasicInfo(data):
    keys = [
        'longName', 'website', 'fullTimeEmployees',
        'marketCap', 'totalRevenue', 'trailingPE', 'sector'
    ]
    return {k: data.get(k, "") for k in keys}

# ---------------- PRICE ----------------
def getPriceHistory(company):
    historyDf = company.history(period='12mo')
    return {
        'price': historyDf['Close'].tolist(),
        'date': historyDf.index.strftime('%Y-%m-%d').tolist()
    }

# ---------------- EARNINGS ----------------
def getEarningsDate(company):
    df = company.earnings_dates
    if df is None or df.empty:
        return []

    now = datetime.now()
    return [
        date.tz_localize(None).strftime('%Y-%m-%d')
        for date in df.index
        if date.tz_localize(None) > now
    ]

# ---------------- NEWS ----------------
def getCompanyNews(company):
    articles = []

    for item in company.news or []:
        content = item.get('content', {})
        title = content.get('title')
        summary = content.get('summary', '')
        url = content.get('canonicalUrl', {}).get('url')

        if title and (summary or url):
            articles.append({
                'title': title,
                'summary': summary,
                'url': url
            })

    return articles

# ---------------- SCRAPING ----------------
def extractArticleBody(url):
    try:
        page = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')

        body_divs = soup.find_all('div', class_='caas-body')
        return " ".join(div.get_text(strip=True) for div in body_divs)
    except Exception:
        return ""

def extractCompanyNewsArticles(newsArticles):
    allText = ""

    for article in newsArticles:
        # Always include summary
        allText += " " + article.get('summary', '')

        # Try scraping full article
        if article.get('url'):
            scraped = extractArticleBody(article['url'])
            allText += " " + scraped

    return allText.strip()

# ---------------- MAIN ----------------
def getCompanyStockInfo(tickerSymbol):
    company = yf.Ticker(tickerSymbol)

    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningDates = getEarningsDate(company)
    newsArticles = getCompanyNews(company)
    newArticlesAllText = extractCompanyNewsArticles(newsArticles)
    newsTextAnalysis = analyze.analyzedText(newArticlesAllText)
    
    finalStockAnalysis = {
        "basicInfo": basicInfo,
        "priceHistory": priceHistory,
        "futureEarningDates": futureEarningDates,
        "newsArticles": newsArticles,
        "newsTextAnalysis":newsTextAnalysis
    }
    return finalStockAnalysis

# comapanyStockAnalysis= getCompanyStockInfo('MSFT')
# print(json.dumps(comapanyStockAnalysis, indent=4))