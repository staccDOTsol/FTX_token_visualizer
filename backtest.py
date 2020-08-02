import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import zipline
from zipline.data.bundles import register

import warnings

plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = [16, 9]
plt.rcParams['figure.dpi'] = 200
warnings.simplefilter(action='ignore', category=FutureWarning)
from zipline.data.bundles.csvdir import csvdir_equities

start_session = pd.Timestamp('2020-01-29', tz='utc')
end_session = pd.Timestamp('2020-07-01', tz='utc')

# register the bundle

register(
    'ftx',  # name we select for the bundle
    csvdir_equities(
        # name of the directory as specified above (named after data frequency)
        ['minutely'],
        # path to directory containing the
        './',
    ),
    calendar_name='XAMS',  # Euronext Amsterdam
    start_session=start_session,
    end_session=end_session
)
