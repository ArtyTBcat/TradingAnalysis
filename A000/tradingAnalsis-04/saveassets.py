from datetime import datetime
import sqlite3
from matplotlib import pyplot as plt
import pandas
from data import client, MarketData
con = sqlite3.connect('assets.db')
cur = con.cursor()

# cur.execute('''CREATE TABLE assets
#                (date text, currency text, free text, lock text, USDAsset text, USD real)''')
# con.commit()
currency = ['BTC','BNB','ETH', 'DOGE','ADA','XRP','SOL','TRX','VET','FTM','DOT','LTC','ATOM', 'MATIC', 'AVAX', 'LUNA', 'LINK'
            , 'COTI', 'ALGO', 'RAY', 'POND', 'FTT']

class saveassets:
    def insertdata(self):
        print("\nRunning Save Assets_Program")
        var = {'currency': [], 'free' : [], 'locked': [], 'USD': []}
        var['USD'].append(float(client.get_asset_balance(asset='USDT')['free']) + float(client.get_asset_balance(asset='USDT')['locked']) )
        for x in range(len(currency)):
            free = client.get_asset_balance(asset=currency[x])['free']
            locked = client.get_asset_balance(asset=currency[x])['locked']
            var['currency'].append(currency[x])
            var['free'].append(free)
            var['locked'].append(locked)
            var['USD'].append((float(free) + float(locked))* float(MarketData(currency[x]).price))

        insert = ("INSERT INTO assets values(?,?,?,?,?)")
        cur.execute(insert, (  str(datetime.now().strftime("%d %B %Y")), str(var['currency']), str(var['free']), str(var['locked']), sum(var['USD'])))
        con.commit()
        print(datetime.now().strftime("%d %B %Y"), "successfully save Assets")

    def getdata(plot=False):
        data = []
        func = {'Date': [], 'USD': [], 'currencyAssets': []}
        for row in cur.execute('SELECT * FROM assets'):
            data.append(row)
            func['Date'].append(row[0])
            func['USD'].append(row[4])
        print(pandas.DataFrame(data))        
        if plot == True:
            for x in range(len(currency)):
                USDassets = (float(client.get_asset_balance(asset=currency[x])['free']) + float(client.get_asset_balance(asset=currency[x])['locked']))* float(MarketData(currency[x]).price)
                func['currencyAssets'].append(USDassets)
            func['currencyAssets'].append(float(client.get_asset_balance(asset='USDT')['free'])+ float(client.get_asset_balance(asset='USDT')['locked']))
            
            pieVal = {'pieval': [], 'labelcurrency': []}            
            for x in range(len(func['currencyAssets'])):
                if int((func['currencyAssets'][x] / sum(func['currencyAssets'])) *100) != 0:
                    pieVal['pieval'].append( float((func['currencyAssets'][x] / sum(func['currencyAssets'])) *100))
                    try: pieVal['labelcurrency'].append(currency[x])
                    except: pieVal['labelcurrency'].append("USDT")
            
            lablecurrency = currency
            lablecurrency.append("USDT")
            fig, (assetsUsd, ax2) = plt.subplots(2)
            plt.title("Crypto_Assets(USD)")
            assetsUsd.plot(func['Date'], func['USD']) #AssetsUSD
            assetsUsd.legend(['AssetsUSD'])
            ax2.pie(pieVal['pieval'], autopct='%1.1f%%', labels = pieVal['labelcurrency'])
            plt.show()

# saveassets.insertdata(0)
saveassets.getdata(True)

