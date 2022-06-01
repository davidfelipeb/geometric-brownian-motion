import numpy as np 
import matplotlib.pyplot as plt

def sn_random_numbers(shape, antithetic=True, moment_matching=True,fixed_seed=False):
    if fixed_seed:
        rng = np.random.default_rng(123)
    else:
        rng = np.random.default_rng()
    
    if antithetic:
        ran = rng.standard_normal((shape[0], shape[1], int(shape[2]/2.)))
        ran = np.concatenate((-ran,ran), axis = 2)
    else:
        ran = rng.standard_normal(shape)
    
    if moment_matching:
        ran = ran - np.mean(ran)
        ran = ran / np.std(ran)
    
    if shape[0] == 1:
        ran = ran[0]
        return ran
    else:
        return ran

def set_mpl_style():
    tsize = 12
    tdir = 'in'
    major = 5.0
    minor = 3.0
    style = 'default'
    plt.style.use(style)
    plt.rcParams['text.usetex'] = True
    plt.rcParams['legend.fontsize'] = tsize
    plt.rcParams['xtick.direction'] = tdir
    plt.rcParams['ytick.direction'] = tdir
    plt.rcParams['xtick.major.size'] = major
    plt.rcParams['xtick.minor.size'] = minor
    plt.rcParams['ytick.major.size'] = major
    plt.rcParams['ytick.minor.size'] = minor