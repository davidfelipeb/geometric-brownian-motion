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

    menv_gbm.add_constant('initial_value', 5)
    menv_gbm.add_constant('volatility'   , 0.2)
    menv_gbm.add_constant('final_date'   , dt.datetime(2022,12,31))
    menv_gbm.add_constant('currency'     , 'USD')
    menv_gbm.add_constant('frequency'    , 'D')
    menv_gbm.add_constant('paths'        , 10)

    csr = constant_short_rate('csr', 0.05)
    menv_gbm.add_curve('discount_curve', csr)
    gbm = geometric_brownian_motion('gbm', menv_gbm)

    gbm.generate_time_series()

    # First Path
    paths_1 = gbm.get_instrument_values(fixed_seed=False)
    vol1 = gbm.volatility

    gbm.update(volatility=0.8)
    paths_2 = gbm.get_instrument_values(fixed_seed=False)
    vol2 = gbm.volatility

    set_mpl_style()

    fig, ax = plt.subplots()
    p1 = ax.plot(gbm.time_series, paths_1[:,:20], ls = '-', lw = 1)
    #p2 = ax.plot(gbm.time_series, paths_2[:,:20], ls = '-', lw = 1, color = 'red')
    ax.legend([p1[0]], [f"Low Volatility ({vol1})"], loc = 'upper left')
    ax.set_xlabel(r'$\mathrm{Time}$', fontsize = 14)
    ax.set_ylabel(r'$\mathrm{Price}$', fontsize = 14)
    ax.set_title(r'$\mathbf{Geometric \ Brownian \ Motion}$', fontsize = 14)
    fig.tight_layout()
    fig.savefig('outputs/test_low.png')

    fig, ax = plt.subplots()
    p2 = ax.plot(gbm.time_series, paths_2[:,:20], ls = '-', lw = 1)
    ax.legend([p2[0]], [f"High Volatility ({vol2})"], loc = 'upper left')
    ax.set_xlabel(r'$\mathrm{Time}$', fontsize = 14)
    ax.set_ylabel(r'$\mathrm{Price}$', fontsize = 14)
    ax.set_title(r'$\mathbf{Geometric \ Brownian \ Motion}$', fontsize = 14)
    fig.tight_layout()
    fig.savefig('outputs/test_high.png')

    fig, ax = plt.subplots()
    p1 = ax.plot(gbm.time_series, paths_1[:,:20], ls = '-', lw = 1, color = 'blue')
    p2 = ax.plot(gbm.time_series, paths_2[:,:20], ls = '-', lw = 1, color = 'red')
    ax.legend([p1[0],p2[0]], [f"Low Volatility ({vol1})",f"High Volatility ({vol2})"], loc = 'upper left')
    ax.set_xlabel(r'$\mathrm{Time}$', fontsize = 14)
    ax.set_ylabel(r'$\mathrm{Price}$', fontsize = 14)
    ax.set_title(r'$\mathbf{Geometric \ Brownian \ Motion}$', fontsize = 14)
    fig.tight_layout()
    fig.savefig('outputs/test_lowhigh.png')

if __name__ == '__main__':
    main()
