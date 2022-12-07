from time import sleep
import pandas as pd
import numpy as np

# The market_environment class is a container for all the market data that is
# needed for the modelling of a financial instrument
class market_environment(object):
    def __init__(self, name, pricing_date):
        
        self.name         = name
        self.pricing_date = pricing_date

        self.constants = {}
        self.arrays    = {}
        self.curves    = {}

    def add_constant(self, key, constant):
        """
        It adds a constant to the list of constants
        
        Args:
          key: The name of the constant.
          constant: The constant value to be added to the input.
        """
        self.constants[key] = constant

    def get_constant(self, key):
        """
        It returns the value of the constant with the given key
        
        Args:
          key: The key of the constant you want to get.
        
        Returns:
          The value of the key in the constants dictionary.
        """
        return self.constants[key]

    def add_array(self, key, array_object):
        """
        It adds an array to the arrays dictionary
        
        Args:
          key: The name of the array.
          array_object: The array object to be added to the dictionary.
        """
        self.arrays[key] = array_object

    def get_array(self, key):
        """
        It returns the array with the given key
        
        Args:
          key: The name of the array.
        
        Returns:
          The array with the key that is passed in.
        """
        return self.arrays[key]

    def add_curve(self, key, curve):
        """
        It adds a curve to the plot
        
        Args:
          key: The name of the curve.
          curve: The curve to add.
        """
        self.curves[key] = curve

    def get_curve(self, key):
        """
        It returns the curve with the given key
        
        Args:
          key: The key of the curve to get.
        
        Returns:
          The curve with the key that is passed in.
        """
        return self.curves[key]

    def add_environment(self, env):
        """
        It adds the constants, arrays, and curves from the input environment to the
        current environment
        
        Args:
          env: the environment to add to the current environment
        """
        for key in env.constants:
            self.constants[key] = env.constants[key]

        for key in env.arrays:
            self.arrays[key] = env.arrays[key]

        for key in env.curves:
            self.curves[key] = env.curves[key]

    def info(self):
        """
        Prints all info related to the market environment
        """
        print(f"{'Name:'} {self.name:>12}")
        print('\nConstants:')
        for key, value in self.constants.items():
            print(f"{key:<10} {str(value):>12}")
        print('\nArrays:')
        for key, value in self.arrays.items():
            print(f"{key:<10} {'dims:',len(value):>12}")

        print('\nCurvers:')
        for key, value in self.curves.items():
            print(f"{key:<10} {value:>12}")
        

