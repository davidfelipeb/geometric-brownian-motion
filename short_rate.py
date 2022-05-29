import numpy as np
import datetime
import datetime as dt

class constant_short_rate(object):
    def __init__(self, name, short_rate):
        self.name = name
        self.short_rate = short_rate
        if short_rate < 0:
            raise ValueError("Short rate negative.")

    def get_year_deltas(self, date_list, day_count = 365):
        start = date_list[0]
        delta_list = [(date - start).days / day_count for date in date_list]
        return np.array(delta_list)

    def get_discount_factors(self, date_list, dtobjects=True):
        if dtobjects is True:
            dlist = self.get_year_deltas(date_list)
        else:
            dlist = np.array(date_list)
        
        dflist = np.exp(self.short_rate * np.sort(-dlist))
        
        return np.array((date_list, dflist)).T


