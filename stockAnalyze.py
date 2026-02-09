import yfinance as yf
from datetime import datetime  

def extractBasicInfo(data):
    keysToExtract = [
        'longName', 'website', 'fullTimeEmployees',
        'marketCap', 'totalRevenue', 'trailingPE', 'sector'
    ]
    return {key: data.get(key, "") for key in keysToExtract}

def getPriceHistory(company):
    historyDf = company.history(period='12mo')

    return {
        'price': historyDf['Close'].tolist(),
        'date': historyDf.index.strftime('%Y-%m-%d').tolist()
    }

def getEarningsDate(company):
    earningsDateDf = company.earnings_dates

    if earningsDateDf is None or earningsDateDf.empty:
        return []

    currentDate = datetime.now()

    futureDates = [
        date.tz_localize(None).strftime('%Y-%m-%d')
        for date in earningsDateDf.index
        if date.tz_localize(None) > currentDate
    ]
    return futureDates

def getCompanyNews(company):
    allNewsArticles = []
    for newsDict in company.news or []:
        title = newsDict.get('title')
        link = newsDict.get('link')

        if not title or not link:
            continue

        allNewsArticles.append({
            'title': title,
            'link': link
        })
    return allNewsArticles

def companyStockInfo(tickerSymbol):

    # Get data from Yahoo Finance
    company = yf.Ticker(tickerSymbol)

    # Get Basic info on Company
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningDates = getEarningsDate(company)
    newsArticles = getCompanyNews(company)


companyStockInfo('MSFT')