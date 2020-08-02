import os
from zipline.utils.run_algo import load_extensions
from zipline.api import get_datetime
load_extensions(
	default=True,
	extensions=[],
	strict=True,
	environ=os.environ,
)
from datetime import date, timedelta
from zipline.data import bundles
import threading, Queue

	
bundle = bundles.load('ftx')
bundle.asset_finder.retrieve_all(bundle.asset_finder.sids)

# imports
from zipline.api import order, order_value, symbol, record, set_benchmark, get_datetime
from zipline.protocol import Portfolio
# parameters


import pandas as pd
import os
lts = ['ADABULL/USD', 'ALGOBULL/USD', 'ALTBULL/USD', 'ATOMBULL/USD', 'BALBULL/USD', 'BCHBULL/USD', 'BNBBULL/USD', 'BSVBULL/USD', 'BTMXBULL/USD', 'BULL/USD', 'COMPBULL/USD', 'DEFIBULL/USD', 'DOGEBULL/USD', 'DRGNBULL/USD', 'EOSBULL/USD', 'ETCBULL/USD', 'ETHBULL/USD', 'EXCHBULL/USD', 'HTBULL/USD', 'KNCBULL/USD', 'LEOBULL/USD', 'LINKBULL/USD', 'LTCBULL/USD', 'MATICBULL/USD', 'MIDBULL/USD',  'OKBBULL/USD', 'PAXGBULL/USD', 'PRIVBULL/USD', 'THETABULL/USD', 'TOMOBULL/USD', 'TRXBULL/USD', 'TRYBBULL/USD',  'XAUTBULL/USD', 'XRPBULL/USD', 'XTZBULL/USD']

import datetime
assets = []
has_ordereds = {}
prices = {}
priceStarts = {}
has_exits = {}
firsts = {}
weekdays = {}
for lt in lts:
	lt = lt.split('/')[0]
	selected_stock = lt
	assets.append(lt	)
	has_ordereds[lt	]=(False)
	has_exits[lt	]=(False)
	prices[lt	]=(None)
	priceStarts[lt	]=(None)
	firsts[lt	]=(True)
	weekdays[lt	]=(0)

def initialize(context):
	context.assets = assets
	context.has_ordereds = has_ordereds 
	context.has_exits = has_exits 
	context.prices = prices
	context.priceStarts = priceStarts
	context.firsts = firsts
	context.deltas = []
	context.weekdays = weekdays
from time import sleep

def handle_data(context, data):
	
		#q.put(None)		
	# record price for further inspection

	dtand10 = get_datetime() + timedelta(minutes=10)
	for lt in lts:
		try:
			selected_stock = lt.split('/')[0]
			asset = symbol(selected_stock)
			wd = (dtand10).weekday()
			pos = context.portfolio.positions
			abs_capital_used = sum(abs(pos[s].amount) * pos[s].cost_basis for s in pos)  
			anamount = 0
			for p in pos:
				#print(pos[p].asset)
				if pos[p].asset == asset:
					anamount = pos[p].amount
			#if anamount != 0:
			#	print(anamount)
			if wd != context.weekdays[selected_stock]:
				context.firsts[selected_stock] = True
				
				if anamount is not 0:
					print(1)
					print(selected_stock)
					print((dtand10))

					print(anamount)
					port = context.portfolio 
					print(port.starting_cash)
					print(port.portfolio_value)
					print(port.cash)
					print(abs_capital_used)
					pt = 0
					for p in pos:
						if pos[p].amount is not 0:
							pt = pt + 1
					print(pt)
					context.deltas = []
					#print(pos[asset].amount)
					context.has_ordereds[selected_stock] = False
					context.has_exits[selected_stock] = False
					order(asset, -1 * anamount)
					
					# setting up a flag for holding a position
					
				context.weekdays[selected_stock] = wd
				return
			else:
				if data.current(asset, 'price') > 0:
					context.prices[selected_stock] = data.current(asset, 'price')
					#record(price=context.prices[selected_stock])
					#if 'BTCBULL' in selected_stock:
					#	record(benchmark=context.prices[selected_stock])
					if context.firsts[selected_stock] == True:

						context.priceStarts[selected_stock] = context.prices[selected_stock]
						context.firsts[selected_stock] = False

					delta = -1 * (1-(context.prices[selected_stock] / context.priceStarts[selected_stock])) * 100
					context.deltas.append(delta)

					tp = 0
					cp = 0
					tn = 0
					cn = 0
					for adelta in context.deltas:
						if adelta > 0:
							tp = tp + adelta
							cp = cp + 1
						elif adelta < 0:
							tn = tn = adelta
							cn = cn + 1
					avgdelta = 0
					if delta < 0:
						avgdelta = tn / cn
					elif delta > 0:
						avgdelta = tp / cp
					
					
					
					#print(abs_capital_used)
					#record(abs_cap_used = abs_capital_used)  
					# calculate free cash: starting_cash + pnl - capital_used  
					port = context.portfolio  
					#print(port)
					abs_cash = port.starting_cash + port.pnl - abs_capital_used  
					#record(abs_cash = abs_cash)  
					qty = port.portfolio_value / 100
					qty = qty / context.prices[selected_stock]
					#print(qty)
					# trading logic
					if not context.has_ordereds[selected_stock]:
						delta = -1 * (1-(context.prices[selected_stock] / context.priceStarts[selected_stock])) * 100
						#print(delta)
						if delta > 10:
							#print('ordering')
							#print(abs_cash)
							# placing order, negative number for sale/short
							context.has_ordereds[selected_stock] = True
							order(asset,  qty)
							return
							# setting up a flag for holding a position
							
						elif delta < -10:

							#print(context.prices[selected_stock])
							#print('ordering')
							#print(abs_cash)
							qty = qty * -1
							# placing order, negative number for sale/short
							context.has_ordereds[selected_stock] = True
							order(asset,  qty)
							return
							# setting up a flag for holding a position
						#else:
							#q.put(None)	
					if anamount is not 0 and context.has_exits[selected_stock] == False:
						
						delta = -1 * (1-(context.prices[selected_stock] / context.priceStarts[selected_stock])) * 100
						if delta < 7 and delta > -7:
							context.has_exits[selected_stock] = True
							# placing order, negative number for sale/short
							#print(qty)
							#print('delta out')
							order(asset, -1 * anamount)
							return
							# setting up a flag for holding a position
							#context.has_ordereds[selected_stock] = False
						#else:
							#q.put(None) 
				else:
					pos = context.portfolio.positions

					
					abs_capital_used = sum(abs(pos[s].amount) * pos[s].cost_basis for s in pos)  
					#print(abs_capital_used)
					#record(abs_cap_used = abs_capital_used)  
					# calculate free cash: starting_cash + pnl - capital_used  
					port = context.portfolio  
					#print(port)
					abs_cash = port.starting_cash + port.pnl - abs_capital_used  
					context.firsts[selected_stock] = True
					if anamount is not 0:
						print(pos)
						print(dtand10)

						print(anamount)
						port = context.portfolio 
						print(port.starting_cash)
						print(port.portfolio_value)
						print(port.cash)
						print(abs_capital_used)
						pt = 0
						for p in pos:
							if pos[p].amount is not 0:
								pt = pt + 1
						print(pt)
						context.deltas = []
						#print(pos[asset].amount)
						context.has_ordereds[selected_stock] = False
						context.has_exits[selected_stock] = False
						order(asset, -1 * anamount)
		except Exception as e:
			print(e)
			sleep(100)	