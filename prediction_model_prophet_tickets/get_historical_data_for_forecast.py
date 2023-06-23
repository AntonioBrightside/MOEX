import MOEX_API

tickers = ['GAZP', 'HYDR', 'MTSS', 'YNDX', 'SBER']

for ticker in tickers:
    result = MOEX_API.get_historical_data('2018-01-01', ticker)

    with open(rf'D:\1. Other\1. Work\1. Programming\1. Projects\MOEX\prediction_model_prophet_tickets\API data\{ticker}.csv', 'w') as f:
        for i in result:
            f.write(str(i) + ',')
        print(f'{ticker} is done! Information has been saved')
