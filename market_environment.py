from time import sleep
import pandas as pd
import numpy as np

class market_environment(object):
    def __ini__(self, name, pricing_date):
        
        self.name         = name
        self.pricing_date = pricing_date

        self.constants = {}
        self.arrays     = {}
        self.curves    = {}

    def add_constant(self, key, constant):
        self.constants[key] = constant

    def get_constant(self, key):
        return self.constants[key]

    def add_array(self, key, array_object):
        self.arrays[key] = array_object

    def get_array(self, key):
        return self.arrays[key]

    def add_curve(self, key, curve):
        self.curves[key] = curve

    def add_environment(self, env):
        for key in env.constants:
            self.constants[key] = env.constants[key]

        for key in env.arrays:
            self.arrays[key] = env.arrays[key]

        for key in env.curves:
            self.curves[key] = env.curves[key]

class simulation(object):

    def __init__(self, name, market_env, corr):
        try:
            self.name = name
            self.pricing_date = market_env.pricing_date
            self.final_date = market_env.get_constant('final_date')
            self.initial_value = market_env.get_constant('initial_value')
            self.volatility = market_env.get_constant('volatility')
            self.currency = market_env.get_constant('currency')
            self.frequency = market_env.get_constant('frequency')
            self.paths = market_env.get_constant('paths')
            self.discount_curve = market_env.get_constant('discount_curve')

            try:
                self.time_series = market_env.get_array('time_series')
            except:
                self.time_series = None

            try:
                self.special_dates = market_env.get_array('specia_dates')
            except:
                self.special_dates = []

            self.instrument_values = None
            self.correlated = corr

            if corr is True:
                self.cholesky_matrix = market_env.get_array('cholesky_matrix')
                self.rn_set = market_env.get_array('rn_set')[self.name]
                self.random_numbers = market_env.get_array('random_numbers')
            
        except :
            print("Error getting Market Environment details.")

    def generate_time_series(self):
        start = self.pricing_date
        end   = self.final_date

        time_series = pd.date_range(start = start, end = end, freq = self.frequency)
        time_series = list(time_series)

        if start not in time_series:
            time_series.insert(0, start)
        if end not in time_series:
            time_series.append(end)
        if len(self.special_dates > 0):
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

class geometric_brownian_motion(simulation):
    def __init__(self, name, market_env, corr = False):
        super().__init__(name, market_env, corr)
    
    def update(self, initial_value = None, volatility = None, final_date = None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if final_date is not None:
            self.final_date = final_date

    def generate_paths(self, fixed_seed = False, day_count = 365):
        if self.time_series is None:
            self.generate_time_series()

        M = len(self.time_series)
        J = self.paths

        paths = np.zeros((M,J))
        paths[0] = self.initial_value

        if not self.correlated:
            if fixed_seed:
                rng = np.random.default_rng(123)
                rand = rng.standard_normal((1,M,J))
            else:
                rng = np.random.default_rng()
                rand = rng.standard_normal((1,M,J))

        else:
            rand = self.random_numbers
        
        short_rate = self.discount_curve.short_rate
        
        for t in range(len(self.time_grid)):
            if not self.correlated:
                rand = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                rand = self[self.rn_set]
            dt = (self.time_series[t] - self.time_series[t-1]).days/day_count
            paths[t] = paths[t-1] * np.exp((short_rate - 0.5*self.volatility**2) + self.volatility * np.sqrt(dt) * ran)
        
        self.instrument_values = paths