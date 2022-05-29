import numpy as np 

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