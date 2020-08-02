import ccxt
ftx = ccxt.ftx({})
lts = []

import pandas as pd
import os
markets = ftx.fetchMarkets()

for market in markets:
	if 'BULL/USD' in market['id'] and 'USDT' not in market['id']:
		##print(market)\

		#ords		= self.binance.fetchOpenOrders( )
		##print(ords)
		lts.append(market['id'])
print(lts)
from time import sleep
sleep(600)
import datetime
for lt in lts:
	towrite = []

	with open('minutely/' + lt.split('/')[0] + '.csv', 'r') as myfile:
		data = myfile.read().split('\n')
		for d in data:
			d = d.split(',')
			#print(d[0])
			try:
				readable = datetime.datetime.fromtimestamp(round(int(d[0]) / 1000)).isoformat()

				d[0] = str(readable)
				writepath = lt.split('/')[0]  + '.csv'
				mode = 'a' if os.path.exists(writepath) else 'w'
				with open(lt.split('/')[0] + '.csv', mode) as myfile2:
					myfile2.write(','.join(str(e) for e in d) + '\n')
			except:
				a = 1