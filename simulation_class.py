import pandas as pd
import numpy as np
import datetime as dt

class simulation_class(object):

    def __init__(self, name, market_env, corr):
        try:
            self.name = name 
            self.pricing_date   = market_env.pricing_date
            self.final_date     = market_env.get_constant('final_date')
            self.initial_value  = market_env.get_constant('initial_value')
            self.volatility     = market_env.get_constant('volatility')
            self.currency       = market_env.get_constant('currency')
            self.frequency      = market_env.get_constant('frequency')
            self.paths          = market_env.get_constant('paths')
            self.discount_curve = market_env.get_curve('discount_curve')
            try:
                self.time_series = market_env.get_array('time_series')
            except:
                self.time_series = None

            try:
                self.special_dates = market_env.get_array('special_dates')
            except:
                self.special_dates = []

            self.instrument_values = None
            self.correlated = corr

            if corr is True:
                self.cholesky_matrix = market_env.get_array('cholesky_matrix')
                self.rn_set = market_env.get_array('rn_set')[self.name]
                self.random_numbers = market_env.get_array('random_numbers')
            print('Succesfully loaded Market Environment')
        except :
            print("Error getting Market Environment details.")

    def generate_time_series(self):
        start = self.pricing_date
        end   = self.final_date

        time_series = pd.date_range(start = start, end = end, freq = self.frequency)
        time_series = [t.to_pydatetime() for t in time_series]

        if start not in time_series:
            time_series.insert(0, start)
        if end not in time_series:
            time_series.append(end)
        if len(self.special_dates) > 0:
            time_series.extend(self.special_dates)
            # Detele repeated dates in case there are 
            time_series = list(set(time_series)) 
            time_series.sort()
        self.time_series = np.array(time_series)

    def get_instrument_values(self, fixed_seed = True):
        if self.instrument_values is None:
            self.generate_paths(fixed_seed = fixed_seed, day_count = 365)
        elif fixed_seed is False:
            self.generate_paths(fixed_seed = fixed_seed, day_count = 365)
        return self.instrument_values