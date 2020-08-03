threshold = 10
testing = True

import ccxt
import pytz
from datetime import datetime, timedelta
utc = pytz.utc
from time import sleep


import os
ftx	  = ccxt.ftx({
				'enableRateLimit': True,
				'apiKey': os.environ['ftxkey'],	
				'secret': os.environ['ftxsecret'],
		  })
print(dir(ftx))
bulls = []
bears = []
lts = []

winners = {}
winners['bull'] = {}
winners['bear'] = {}
losers = {}
precisions = {}
losers['bull'] = {}
losers['bear'] = {}
wd = -1
dttarget = None
wdchanges = 0
mids = {}
bl = ["ALGOBEAR/USD"]
def reload():

	global bl, dttarget, wdchanges, wd, losers, winners, lts, bears, bulls, ftx, mids, precisions, threshold
	dt = datetime.now(tz=utc) + timedelta(minutes=10)
	#print (datetime.now(tz=utc) < dt)
	dtwd = dt.weekday()
	gogo = True
	if wdchanges < 2 and testing == False:#2
		gogo = False
		print('gogo false! wd changecount needs to be 2+! It\'s ' + str(wdchanges))
	markets = ftx.fetchMarkets()

	for market in markets:
		if 'BULL/USD' in market['id'] and 'USDT' not in market['id']:
			precisions[market['id']] = (market['precision'])
			mids[market['id']] = (market['info']['bid'] + market['info']['ask']) / 2
			delta = (market['info']['changeBod'] * 100)
			if delta > 0:
				winners['bull'][market['id']] = delta
			elif delta < 0:
				losers['bull'][market['id']] = delta
			#ords		= binance.fetchOpenOrders( )
			##print(ords)
			if market['id'] not in lts:
				bulls.append(market['id'])
				lts.append(market['id'])
		elif 'BEAR/USD' in market['id'] and 'USDT' not in market['id']:
			precisions[market['id']] = (market['precision'])
			mids[market['id']] = (market['info']['bid'] + market['info']['ask']) / 2
			delta = (market['info']['changeBod'] * 100)
			if delta > 0:
				winners['bear'][market['id']] = delta
			elif delta < 0:
				losers['bear'][market['id']] = delta
			##print(market)\

			#ords		= binance.fetchOpenOrders( )
			##print(ords)
			if market['id'] not in lts:
				bears.append(market['id'])
				lts.append(market['id'])
	if dtwd != wd:
		dttarget = datetime.now(tz=utc) + timedelta(minutes=35)
		positions		= ftx.privateGetLtBalances()['result']
		obj = {}
		for pos in positions:
			obj[pos['coin'] + '/USD'] = pos
			
		print(dtwd)
		wd = dtwd
		wdchanges = wdchanges + 1

		for lt in lts:
			try:
				if lt in obj:
					if obj[lt]['usdValue'] > 1 and lt not in bl:
						print('exit 1')
						print(obj[lt])
						qty = obj[lt]['total']
						o = ftx.createOrder(lt, 'market', 'sell', qty)
						#o = ftx.privatePostLtTokenNameRedeem({'token_name': lt.split('/')[0], 'size': qty})
						print(o)

						#return
						#sleep(10)
			except Exception as e:
				print(e)
	if (gogo == True and datetime.now(tz=utc) > dttarget) or testing == True:	
		print(1)
		bal2 = ftx.fetchBalance()
		newbal = 0
		#print(bal2)
		#print(bal2)
		for coin in bal2['info']['result']:
			newbal = newbal + coin['usdValue']
		bal = newbal
		positions		= ftx.privateGetLtBalances()['result']
		obj = {}
		for pos in positions:
			obj[pos['coin'] + '/USD'] = pos
		#print(obj)
		for bullbear in winners:
			for lt in winners[bullbear]:
				if winners[bullbear][lt] > threshold:
					if lt not in obj and lt not in bl:
						print('exit 2')
						print(lt)
						qty = bal * 1 * 0.03 
						print(qty)
						qty = qty / mids[lt]
						print(qty)
						precision = precisions[lt]['amount']
						
						print(precision)
						qty = round(qty / precision)* precision
						print(qty)
						if precision >= 1:
							qty = int(qty)
						qty = float(qty)
						print(qty)
						o = ftx.createOrder(lt, 'market', 'buy', qty)#o = ftx.privatePostLtTokenNameCreate({'token_name': lt.split('/')[0], 'size': qty})
						print(o)


						return
						#sleep(10)
					if lt in obj:
						if obj[lt]['usdValue'] <= 1 and lt not in bl:
							print('exit 3')
							print(lt)
							qty = bal * 1 * 0.03 
							print(qty)
							qty = qty / mids[lt]
							print(qty)
							precision = precisions[lt]['amount']
							print(precision)
							qty = round(qty / precision)* precision
							print(qty)
							if precision >= 1:
								qty = int(qty)
							qty = float(qty)
							print(qty)
							print({'token_name': lt.split('/')[0], 'size': qty})
							o = ftx.createOrder(lt, 'market', 'buy', qty)#o = ftx.privatePostLtTokenNameCreate({'token_name': lt.split('/')[0], 'size': qty})
							print(o)

							return
							#sleep(10)
				if lt in obj:
					if lt not in bl and obj[lt]['usdValue'] > 1 and winners[bullbear][lt] < threshold / 10 * 5:

						print('exit 4')
						qty = obj[lt]['total']
						o = ftx.createOrder(lt, 'market', 'sell', qty)#o = ftx.privatePostLtTokenNameRedeem({'token_name': lt.split('/')[0], 'size': qty})
						print(o)

						return
						#sleep(10)
	"""
	for bullbear in losers:
		for lt in losers[bullbear]:

			if losers[bullbear][lt] < -1 * threshold:
				
				if lt not in obj:
					qty = bal * 1 * 0.03 
					print('exit 5')
					print(lt)
					print(qty)
					qty = qty / mids[lt]
					print(qty)
					precision = precisions[lt]['amount']
					print(precision)
					qty = round(qty / precision)* precision
					print(qty)
					if precision >= 1:
						qty = int(qty)
					qty = float(qty)
					print(qty)
					o = ftx.createOrder(lt, 'market', 'buy', qty)#o = ftx.privatePostLtTokenNameCreate({'token_name': lt.split('/')[0], 'size': qty})
					print(o)

					return
					#sleep(10)
				elif obj[lt]['usdValue'] <= 1:
					print('exit 6')
					qty = bal * 1 * 0.03 
					print(lt)
					print(qty)
					qty = qty / mids[lt]
					print(qty)
					precision = precisions[lt]['amount']
					
					print(precision)
					qty = round(qty / precision)* precision
					if precision >= 1:
						qty = int(qty)
					qty = float(qty)
					print(qty)
					o = ftx.createOrder(lt, 'market', 'buy', qty)#o = ftx.privatePostLtTokenNameCreate({'token_name': lt.split('/')[0], 'size': qty})
					print(o)

					return
					#sleep(10)
			if lt in obj:
				if obj[lt]['usdValue'] > 1 and losers[bullbear][lt] > -1 * threshold / 10 * 5:
					qty = obj[lt]['total']
					print('exit 7')
					o = ftx.createOrder(lt, 'market', 'sell', qty)#o = ftx.privatePostLtTokenNameRedeem({'token_name': lt.split('/')[0], 'size': qty})
					print(o)

					return
					#sleep(10)
"""
while True:
	reload()
	sleep(5)
import time;
import os


import threading
