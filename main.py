from importlib.resources import path

from matplotlib import markers
from market_environment import *
from geometric_brownian_motion import *
from short_rate import *

import matplotlib.pyplot as plt

def main():
    # Working Example

    # Set market environment and its attributes
    menv_gbm = market_environment('me_gbm', dt.datetime(2022,1,1))

    menv_gbm.add_constant('initial_value', 36)
    menv_gbm.add_constant('volatility'   , 0.1)
    menv_gbm.add_constant('final_date'   , dt.datetime(2022,12,31))
    menv_gbm.add_constant('currency'     , 'USD')
    menv_gbm.add_constant('frequency'    , 'M')
    menv_gbm.add_constant('paths'        , 10)

    csr = constant_short_rate('csr', 0.05)
    menv_gbm.add_curve('discount_curve', csr)
    gbm = geometric_brownian_motion('gbm', menv_gbm)

    gbm.generate_time_series()

    # First Path
    paths_1 = gbm.get_instrument_values(fixed_seed=False)
    vol1 = gbm.volatility

    gbm.update(volatility=0.5)
    paths_2 = gbm.get_instrument_values(fixed_seed=False)
    vol2 = gbm.volatility

    fig, ax = plt.subplots()
    p1 = ax.plot(gbm.time_series, paths_1[:,:20], ls = '-', lw = 1, color = 'blue', marker = 'o')
    p2 = ax.plot(gbm.time_series, paths_2[:,:20], ls = '--', lw = 1, color = 'red', marker = 'o')
    ax.legend([p1[0], p2[0]], [f"Low Volatility ({vol1})",f"High Volatility ({vol2})"], loc = 'upper left')
    fig.savefig('outputs/test.png')

if __name__ == '__main__':
    main()
