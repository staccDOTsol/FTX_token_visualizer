import ccxt
ftx = ccxt.ftx({})
lts = []


markets = ftx.fetchMarkets()

for market in markets:
	if 'BULL/USD' in market['id'] and 'USDT' not in market['id']:
		##print(market)\

		#ords		= self.binance.fetchOpenOrders( )
		##print(ords)
		lts.append(market['id'])

import time;
import os

def threadedGather(lt):
	print(lt)
	ts = time.time()
	ts = int(ts) * 1000
	ts = ts - 1000 * 60 * 60 * 24 * 30 * 1
	print(ts)

	
	first = True
	while ts < int(time.time() * 1000- 1000 * 60 * 60 * 24):
		if first != True: 
			print(lt + ': ' + str(ts))
		else:
			first = False
		ohlcvs = ftx.fetchOHLCV(lt, '1m', ts, 1000)#, okex.parse8601 ('2018-11-08T00:00:00'))
		for ohlcv in ohlcvs:
			if ohlcv[0] > ts:
				ts = (ohlcv[0])
			writepath = lt.split('/')[0]  + '.csv'

			mode = 'a' if os.path.exists(writepath) else 'w'
			with open(lt.split('/')[0] + '.csv', mode) as myfile:
				myfile.write(','.join(str(e) for e in ohlcv) + '\n')
		if len(ohlcvs) < 500:
			ts = int(time.time() * 1000)
import threading

for lt in lts:
	x = threading.Thread(target=threadedGather, args=(lt,))
	print(lt)
	x.start()