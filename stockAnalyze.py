# import json
# import yfinance as yf
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime
# import analyze  

# def extractBasicInfo(data):
#     keysToExtract = [
#         'longName', 'website', 'fullTimeEmployees',
#         'marketCap', 'totalRevenue', 'trailingPE', 'sector'
#     ]
#     return {key: data.get(key, "") for key in keysToExtract}

# def getPriceHistory(company):
#     historyDf = company.history(period='12mo')

#     return {
#         'price': historyDf['Close'].tolist(),
#         'date': historyDf.index.strftime('%Y-%m-%d').tolist()
#     }

# def getEarningsDate(company):
#     earningsDateDf = company.earnings_dates

#     if earningsDateDf is None or earningsDateDf.empty:
#         return []

#     currentDate = datetime.now()

#     futureDates = [
#         date.tz_localize(None).strftime('%Y-%m-%d')
#         for date in earningsDateDf.index
#         if date.tz_localize(None) > currentDate
#     ]
#     return futureDates

# def getCompanyNews(company):
#     print("RAW news:", company.news)

#     allNewsArticles = []

#     for newsDict in company.news or []:
#         print("Item:", newsDict)

#         title = newsDict.get('title')
#         link = newsDict.get('link')

#         if not title or not link:
#             print("Skipped item")
#             continue

#         allNewsArticles.append({
#             'title': title,
#             'link': link
#         })

#     return allNewsArticles


# def extractNewsArticleTextFromHtml(soup):
#     allText = ''
#     result = soup.find_all('div', {'class":"caas-body'})
#     for res in result:
#         allText += res.text
#         return allText

# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/119.0.0.0 Safari/537.36'
#     }
# def extraCompanyNewsArticles(newsArticles):
#     allArticlesText = ""
#     for newsArticle in newsArticles:
#         url= newsArticle['link']
#         page = requests.get(url, headers=headers)
#         soup = BeautifulSoup(page.txt, 'html.parser')
#         if not soup.findAll(string="Continue Reading"):
#             allArticlesText += extractNewsArticleTextFromHtml(soup)
#     return allArticlesText
    
# def companyStockInfo(tickerSymbol):
#     # Get data from Yahoo Finance
#     company = yf.Ticker(tickerSymbol)
#     # Get Basic info on Company
#     basicInfo = extractBasicInfo(company.info)
#     priceHistory = getPriceHistory(company)
#     futureEarningDates = getEarningsDate(company)
#     newsArticles = getCompanyNews(company)
#     newArticlesAllText = extraCompanyNewsArticles(newsArticles)
#     newsTextAnalysis = analyze.analyzedText(newArticlesAllText)
#     finalResultJson = json.dumps(newsTextAnalysis,indent=4)

#     # Print for Test
#     print(finalResultJson)

# companyStockInfo('MSFT')

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
def companyStockInfo(tickerSymbol):
    company = yf.Ticker(tickerSymbol)

    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningDates = getEarningsDate(company)
    newsArticles = getCompanyNews(company)
    newArticlesAllText = extractCompanyNewsArticles(newsArticles)
    finalResultJson = analyze.analyzedText(newArticlesAllText)

    print(json.dumps(finalResultJson, indent=4))

companyStockInfo('MSFT')