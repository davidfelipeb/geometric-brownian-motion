from time import sleep
import pandas as pd
import numpy as np

class market_environment(object):
    def __init__(self, name, pricing_date):
        
        self.name         = name
        self.pricing_date = pricing_date

        self.constants = {}
        self.arrays    = {}
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

    def get_curve(self, key):
        return self.curves[key]

    def add_environment(self, env):
        for key in env.constants:
            self.constants[key] = env.constants[key]

        for key in env.arrays:
            self.arrays[key] = env.arrays[key]

        for key in env.curves:
            self.curves[key] = env.curves[key]

    def info(self):
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
        

