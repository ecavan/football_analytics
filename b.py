from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
from twisted.internet import reactor
from time import sleep
import pandas as pd

price = {'BTCUSDT': pd.DataFrame(columns=['date', 'price', 'volume','ma','vma']), 'ETHUSDT': pd.DataFrame(columns=['date', 'price', 'volume','ma','vma']), 'error':False}

def btc_pairs_trade(msg):
    if msg['e'] != 'error':
        price['BTCUSDT'].loc[len(price['BTCUSDT'])] = [pd.Timestamp.now(), float(msg['c']), float(msg['v']), '', '']
    else:
        price['error'] = msg['e']
            
            
def btc_pairs_trade2(msg):
    if msg['e'] != 'error':
        price['ETHUSDT'].loc[len(price['ETHUSDT'])] = [pd.Timestamp.now(), float(msg['c']), float(msg['v']), '', '']
    else:
        price['error']= msg['e']


def create_df():

    bsm = BinanceSocketManager(client)
    conn_key = bsm.start_symbol_ticker_socket('ETHUSDT', btc_pairs_trade2)
    conn_key2 = bsm.start_symbol_ticker_socket('BTCUSDT', btc_pairs_trade)
    bsm.start()

    while len(price['ETHUSDT'])  == 0:
        sleep(0.1)

    sleep(30)
        
    df = price['ETHUSDT']

    return df
