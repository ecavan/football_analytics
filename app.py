from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
from twisted.internet import reactor
from time import sleep
import pandas as pd
from flask import Flask, render_template

api_key_demo = "vFSxpUvEvV2JAknpqBtch1OV4Tfw5dOGcJW91qlIl2sLxHvbZ2JLOqJhB4HsMB4n"
api_secret_demo = "5vEoKn0bu4LDpbtNuUFclEneuJibdxtX5PBGS6crzZESOF6KT3TQ7kf5imKLyKyo"

client = Client(api_key_demo, api_secret_demo)
client.API_URL = 'https://testnet.binance.vision/api'

price = {'BTCUSDT': pd.DataFrame(columns=['date', 'price', 'volume','ma','vma']), 'ETHUSDT': pd.DataFrame(columns=['date', 'price', 'volume','ma','vma']), 'error':False}

def btc_pairs_trade(msg):
    if msg['e'] != 'error':
        price['BTCUSDT'].loc[len(price['BTCUSDT'])] = [pd.Timestamp.now(), float(msg['c']), float(msg['v']), '', '']
    else:
        price['error'] =  True
            
            
def btc_pairs_trade2(msg):
    if msg['e'] != 'error':
        price['ETHUSDT'].loc[len(price['ETHUSDT'])] = [pd.Timestamp.now(), float(msg['c']), float(msg['v']), '', '']
    else:
        price['error'] = True

# x = client.get_account()

# balance = float(x['balances'][6]['free'])
# btc = float(x['balances'][1]['free'])
# eth = float(x['balances'][3]['free'])
# value = balance + 4000*eth + 40000*btc

# p1 = ('Initial Account Balance: ' + str(x['balances'][6]['free']) + "<br/>" 
#                         + 'Initial ETH Balance: ' + str(x['balances'][3]['free']) + "<br/>" 
#                         +  'Initial BTC Balance: ' + str(x['balances'][1]['free']) + "<br/>" 
#                           + 'Initial Approximate Portfolio value: ' + str(value)
#      )


def create_order():
    
    bsm = BinanceSocketManager(client)
    conn_key = bsm.start_symbol_ticker_socket('ETHUSDT', btc_pairs_trade2)
    conn_key2 = bsm.start_symbol_ticker_socket('BTCUSDT', btc_pairs_trade)
    bsm.start()
    
    while len(price['ETHUSDT'])  == 0:
        sleep(0.1)
    
    sleep(20)
    
    x = client.get_account()
    
    balance = float(x['balances'][6]['free'])
    btc = float(x['balances'][1]['free'])
    eth = float(x['balances'][3]['free'])
    value = balance + 4000*eth + 40000*btc
    
    stocks = ['ETHUSDT','BTCUSDT' ]
    
    for stock in stocks:
    
        df = price[stock]

        #df['ma'] = df['price'].ewm(halflife=10).mean()
        df = df.sort_values('date', ascending = False)
        
        try:
            if df.price.iloc[0] >100:
                order = client.order_market_sell(symbol=stock, quantity=0.01)

            elif df.price.iloc[0] < 100:
                order = client.order_market_buy(symbol=stock, quantity=0.01)

            sleep(0.1)
            
        except:
            return 'Error'
    
    y = client.get_account()
    balance_final = float(y['balances'][6]['free'])
    btc_final = float(y['balances'][1]['free'])
    eth_final = float(y['balances'][3]['free'])
    value_final = balance_final + 4000*eth_final + 40000*btc_final
    change_final = 100*((value_final - value)/value)
    
    p1 = ('Initial Approximate Portfolio value: ' + str(value) + "<br/>"  + "<br/>" + 
          'Difference Account Balance: ' + str(float(y['balances'][6]['free']) - float(x['balances'][6]['free'])) + "<br/>" 
                        + 'Difference ETH Balance: ' + str(float(y['balances'][3]['free']) - float(x['balances'][3]['free'])) + "<br/>" 
                            +  'Difference BTC Balance: ' + str(float(y['balances'][1]['free']) - float(x['balances'][1]['free'])) + "<br/>" 
                              + '% Difference Portfolio Value: ' + str(change_final) +'%' + "<br/>"  + "<br/>" +
                                 + 'Final Approximate Portfolio Value: ' + str(value_final)
     )

    
    return 'ok'

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():

  return 'ok'

@app.route('/my-link2/')
def my_link2():

  return create_order()

if __name__ == '__main__':
  app.run(debug=True, use_reloader=False)
  #create_order()
  