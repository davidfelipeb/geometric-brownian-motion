import numpy as np
import datetime
import datetime as dt

# The class `constant_short_rate` implements a constant short rate model
class constant_short_rate(object):
    def __init__(self, name, short_rate):
        """
        The function `__init__` is a special function that is called when an object is
        created. 
        The argument `short_rate` is the short rate of the object. 
        The function `__init__` raises an error if the value of the argument
        `short_rate` is negative.
        
        Args:
          name: The name of the model.
          short_rate: The short rate is the risk-free interest rate.
        """
        self.name = name
        self.short_rate = short_rate
        if short_rate < 0:
            raise ValueError("Short rate negative.")

    def get_year_deltas(self, date_list, day_count = 365):
        """
        > It takes a list of dates as strings, converts them to a list of datetime
        objects, and returns a Numpy array of those dates in terms of years
        
        Args:
          date_list: a list of datetime objects
          day_count: The number of days in a year. Defaults to 365
        
        Returns:
          the number of days between the first date in the list and the current date in
        the list divided by the number of days in a year.
        """
        start = date_list[0]
        delta_list = [(date - start).days / day_count for date in date_list]
        return np.array(delta_list)

    def get_discount_factors(self, date_list, dtobjects=True):
        """
        > The function takes a list of dates and returns a list of discount factors
        
        Args:
          date_list: a list of dates, either as datetime objects or as year fractions
          dtobjects: If True, date_list is a list of Python datetime objects. If False,
        date_list is a list of year fractions. Defaults to True
        
        Returns:
          A list of tuples, each tuple containing a date and the discount factor for
        that date.
        """
        if dtobjects is True:
            dlist = self.get_year_deltas(date_list)
        else:
            dlist = np.array(date_list)
        
        # Compute discount factors
        dflist = np.exp(self.short_rate * np.sort(-dlist))
        
        return np.array((date_list, dflist)).T


