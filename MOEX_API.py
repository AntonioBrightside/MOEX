import requests
import datetime


def status(domain='http://iss.moex.com'):
    """Check connection status"""
    return requests.get(domain)


def get_ticker_general_info(*tickers, keys=('SECID', 'SHORTNAME', 'LATNAME', 'TYPENAME', 'GROUPNAME')):
    """To get general info from API: SECID, SHORTNAME, LATNAME, TYPENAME, GROUPNAME.
    Possible to change keys tuple and get another / additional data"""

    result = []

    for ticker in tickers:
        URL = f'http://iss.moex.com/iss/securities/{ticker}.json'
        r = requests.get(URL, params={'iss.meta': 'off', 'iss.only': 'description',
                                      'iss.json': 'extended',
                                      'description.columns': 'name,title,value'})
        data = r.json()[1]
        for i in data['description']:
            if i['name'] in keys:
                result.append(i['value'])

    return result


def get_current_ticker_price(*tickers, datablock='marketdata', engine='stock', markets='shares', boards='TQBR',
                             columns='SECID, BOARDID, OPEN, LOW, HIGH, LAST, VOLTODAY, NUMTRADES, TIME'):
    """To get current price of securities"""
    result = []

    for ticker in tickers:
        URL = f'http://iss.moex.com/iss/engines/{engine}/markets/{markets}/boards/{boards}/securities/{ticker}.json'
        r = requests.get(URL, params={'iss.meta': 'off', 'iss.only': datablock,
                                      'iss.json': 'extended',
                                      f'{datablock}.columns': columns})

        data = r.json()[1]
        for i in data[datablock]:
            for key in i:
                result.append(i[key])

    return result


def get_current_currency_price(ticker='USD000000TOD', datablock='marketdata', engine='currency', markets='selt',
                               boards='CETS', conclusion=type[list | dict],
                               columns='SECID, BOARDID, HIGH, LOW, OPEN, LAST, VOLTODAY, NUMTRADES, TIME'):
    """To get current price for USDRUB_TOD currency and the others. The data is ~15 minutes behind the real time.
    :argument conclusion: dict (as a default) or list. Return list or dict as a result"""

    result = []

    URL = f'http://iss.moex.com/iss/engines/{engine}/markets/{markets}/boards/{boards}/securities/{ticker}.json'
    r = requests.get(URL, params={'iss.meta': 'off', 'iss.only': datablock,
                                  'iss.json': 'extended',
                                  f'{datablock}.columns': columns})

    data = r.json()[1]

    if conclusion == dict:
        return data['marketdata'][0]
    else:
        for i in data[datablock]:
            for key in i:
                result.append(i[key])
        return result


def get_historical_data(start_date, ticker,
                        datablock='history', engine='stock', market='shares', board='TQBR',
                        columns='TRADEDATE, OPEN, CLOSE'):
    """To get historical stocks data from specific date. Return list of data: date, open, close.
    :argument start_date: should be in string format like '2023-01-01'"""

    result = []

    date = datetime.datetime.now().date()
    days = [date - datetime.timedelta(days=i) for i in range(4)]

    def recursion(start_date, ticker, finish_date=None):

        if finish_date in days:
            return result
        else:
            URL = f'http://iss.moex.com/iss/history/engines/{engine}/markets/{market}/boards/{board}/securities/{ticker}.json'
            r = requests.get(URL, params={'iss.meta': 'off', 'iss.only': datablock,
                                          'iss.json': 'extended',
                                          f'{datablock}.columns': columns,
                                          'from': start_date})

            data = r.json()[1].get(datablock)
            for i in data:
                for key in i:
                    result.append(i[key])

            finish_date = data[len(data) - 1].get('TRADEDATE')
            finish_date = datetime.datetime.strptime(finish_date, '%Y-%m-%d').date()
            recursion(start_date=finish_date, ticker=ticker, finish_date=finish_date)

    recursion(start_date=start_date, ticker=ticker, finish_date=None)
    return result


def get_historical_data_with_end_data(start_date, finish_date, ticker,
                                      datablock='history', engine='stock', market='shares', board='TQBR',
                                      columns='TRADEDATE, OPEN, CLOSE'):
    """To get historical stocks data from specific till specific date.
    Accept only one ticker. Return list of data: date, open, close.
    :argument start_date: should be in string format like '2023-01-01'
    :argument finish_date: should be in string format like '2023-01-03'
    :argument ticker: accept only one ticker"""

    result = []

    finish_date = datetime.datetime.strptime(finish_date, '%Y-%m-%d').date()
    days = [finish_date - datetime.timedelta(days=i) for i in range(4)]
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

    def get_data(start_date=start_date, end_date=None):
        URL = f'http://iss.moex.com/iss/history/engines/{engine}/markets/{market}/boards/{board}/securities/{ticker}.json'
        r = requests.get(URL, params={'iss.meta': 'off', 'iss.only': datablock,
                                      'iss.json': 'extended',
                                      f'{datablock}.columns': columns,
                                      'from': start_date,
                                      'till': end_date})

        data = r.json()[1].get(datablock)
        for i in data:
            for key in i:
                result.append(i[key])

        end_date = data[len(data) - 1].get('TRADEDATE')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        return end_date

    while True:

        end_date = start_date + datetime.timedelta(days=100)

        if finish_date <= end_date:
            end_date = finish_date

        if end_date in days:  # ?
            if end_date in result:
                return result
            else:
                get_data(start_date=start_date, end_date=end_date)
                return result
        else:
            end_date = get_data(start_date=start_date, end_date=end_date)
            start_date = end_date


result = get_historical_data_with_end_data(start_date='2022-01-03', finish_date='2023-06-05', ticker='GAZP')
print(result)
