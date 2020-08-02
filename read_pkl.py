import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import zipline
from trading_calendars import get_calendar
import warnings


buy_and_hold_results = pd.read_pickle('ftx.pickle')
fig, ax = plt.subplots(3, 1, sharex=True, figsize=[16, 9])

# portfolio value
buy_and_hold_results.portfolio_value.plot(ax=ax[0])
ax[0].set_ylabel('Portfolio Returns %')

# mark transactions
perf_trans = buy_and_hold_results.loc[[t != [] for t in buy_and_hold_results.transactions]]
buys = perf_trans.loc[[t[0]['amount'] > 0 for t in perf_trans.transactions]]
sells = perf_trans.loc[[t[0]['amount'] < 0 for t in perf_trans.transactions]]
ax[0].plot(buys.index, buy_and_hold_results.portfolio_value.loc[buys.index], '^', markersize=10, color='g', label='buy')
ax[0].plot(sells.index, buy_and_hold_results.portfolio_value.loc[sells.index], 'v', markersize=10, color='r', label='sell')

# daily returns
buy_and_hold_results.returns.plot(ax=ax[1])
ax[1].set_ylabel('daily returns')

buy_and_hold_results.benchmark.plot(ax=ax[2])
ax[2].set_ylabel('BTCBULL Price')


fig.suptitle('LT Rebalancing Strategy', fontsize=16)
plt.legend()
plt.show()

print('Final portfolio value ($): {}'.format(np.round(buy_and_hold_results.portfolio_value[-1], 2)))
