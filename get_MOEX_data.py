import MOEX_API

# Loading list of BLUE tickers and get / save  API data in local storage
with open(r"D:\1. Other\1. Work\1. Programming\1. Projects\MOEX\data\MOEX. Список Голубых.txt", 'r') as f:
    BLUE = f.read().replace(' ', '').split(sep=',')

with open(r'D:\1. Other\1. Work\1. Programming\1. Projects\MOEX\data\collected\BLUE_gathered_general_ticker_info.txt', 'w') as f:
    for i in MOEX_API.get_ticker_general_info(*BLUE):
        f.write(i + ',')
    print('Blue is Done')

# Loading a list of PREBLUE tickers and get / save  API data in local storage
with open(r"D:\1. Other\1. Work\1. Programming\1. Projects\MOEX\data\MOEX. Список Предголубые.txt", 'r') as f:
    PREBLUE = f.read().replace(' ', '').split(sep=',')

with open(r'D:\1. Other\1. Work\1. Programming\1. Projects\MOEX\data\collected\PREBLUE_gathered_general_ticker_info.txt', 'w') as f:
    for i in MOEX_API.get_ticker_general_info(*PREBLUE):
        f.write(i + ',')
    print('PreBlue is Done')
