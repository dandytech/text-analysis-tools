import yfinance as yf


def extractBasicInfo(data):
    keysToExtract = ['longName', 'website', 'fullTimeEmployees', 'marketCap', 'totalRevenue', 'trailingPE', 'sector']
    basicInfo ={}
    for key in keysToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ""
    return basicInfo

def companyStockInfo(tickerSymbol):
    company =yf.Ticker(tickerSymbol)
    basicInfo =extractBasicInfo(company.info)
    print(basicInfo)

companyStockInfo("MSFT")