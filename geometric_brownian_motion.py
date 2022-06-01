from simulation_class import *
from auxiliary_functions import *
import numpy as np

class geometric_brownian_motion(simulation_class):
    def __init__(self, name, market_env, corr = False):
        super(geometric_brownian_motion, self).__init__(name, market_env, corr)
    
    def update(self, initial_value = None, volatility = None, final_date = None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if final_date is not None:
            self.final_date = final_date

        self.instrument_values = None

    def generate_paths(self, fixed_seed = False, day_count = 365):
        if self.time_series is None:
            self.generate_time_series()

        M = len(self.time_series)
        J = self.paths

        paths = np.zeros((M,J))
        paths[0] = self.initial_value

        if not self.correlated:
            rand = sn_random_numbers((1,M,J), fixed_seed = fixed_seed)

        else:
            rand = self.random_numbers
        
        short_rate = self.discount_curve.short_rate
        
        for t in range(1, len(self.time_series)):
            if not self.correlated:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]

            dt = (self.time_series[t] - self.time_series[t-1]).days/day_count
            paths[t] = paths[t-1] * np.exp((short_rate - 0.5*self.volatility**2) * dt 
                                            + self.volatility * np.sqrt(dt) * ran)
        
        self.instrument_values = paths