from importlib.resources import path
from market_environment import *
from geometric_brownian_motion import *
from short_rate import *

import matplotlib.pyplot as plt
'''
dates = [dt.datetime(2015, 1, 1), dt.datetime(2015, 7, 1),dt.datetime(2016, 1, 1)]
csr = constant_short_rate('csr', 0.05)
print(csr.get_year_deltas(dates))
print(csr.short_rate)
print(csr.get_discount_factors(dates, dtobjects=True))
'''
# Working Example

# Set market environment and its attributes
menv_gbm = market_environment('me_gbm', dt.datetime(2022,1,1))

menv_gbm.add_constant('initial_value', 100)
menv_gbm.add_constant('volatility'   , 0.1)
menv_gbm.add_constant('final_date'   , dt.datetime(2022,12,31))
menv_gbm.add_constant('currency'     , 'USD')
menv_gbm.add_constant('frequency'    , 'M')
menv_gbm.add_constant('paths'        , 10000)

csr = constant_short_rate('csr', 0.05)
menv_gbm.add_curve('discount_curve', csr)
gbm = geometric_brownian_motion('gbm', menv_gbm)

gbm.generate_time_series()

# First Path
paths_1 = gbm.get_instrument_values()
vol1 = gbm.volatility

gbm.update(volatility=0.5)
paths_2 = gbm.get_instrument_values()
vol2 = gbm.volatility

fig, ax = plt.subplots()
ax.plot(gbm.time_series, paths_1[:,:10], color = 'blue')
ax.plot(gbm.time_series, paths_2[:,:10], color = 'red')
#ax.legend()
fig.savefig('outputs/test.png')
