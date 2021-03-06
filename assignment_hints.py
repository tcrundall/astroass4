"""These solutions provide a minimalist answer to the question"""
from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np
import emcee

def v_func(a, t):
    """With a list or numpy array of parameters and t a list of times,
    this function returns the function defined in equation 1. """
    #INSERT CODE HERE!
    return a[0] + a[1]*t + a[2]*np.sin(2*np.pi*(a[3]*t + a[4]))
    
def simulate_v(t_min=0, t_max=1.5, a_in=[0,1,1,1,0], n_points=100, sigma=0.5):
    """Some default keyword arguments, for a function to generate random data"""
    #times = t_min + (t_max - t_min)*SOMETHING_ABOUT_np.random.random
    #v_with_errors = SOMETHING_ABOUT_np.random.normal

    times = np.random.uniform(t_min, t_max, 100)

    v_with_errors = np.random.normal(v_func(a_in, times), sigma)

    return times, v_with_errors
    
def lnprob_v_func(a_try, times, vs, sigma=1.0):
    
    #Compute chi-squared, and return -chi-squared/2
    # - may need to take log of result
    # - higher is better
    # - note that I haven't used sigma for anything

    chi_s = 0
    v_fit = v_func(a_try, times)
    for i in range(len(times)):
      chi_s += (vs[i] - v_fit[i])**2 / v_fit[i]

    return - chi_s / 2.0

if __name__=="__main__":  
    #Simulate our data
    times, v_with_errors = simulate_v()

    #Define some key variables.
    ndim = 5
    nwalkers = 20
    n_burnin = int(1000)
    n_chain = int(10000)

    #Lets make a starting point as a bunch of random numbers
    a_init = np.random.normal( size=(nwalkers,ndim) )

    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob_v_func, args=[times, v_with_errors])
    pos, lnprob, state = sampler.run_mcmc(a_init, n_burnin)

    #A check plot, to see if burn in is complete.
    plt.plot(sampler.lnprobability.T)
    plt.title("Is burn in complete?")
    plt.show()

    #Some helper code to help eliminate the worst chains: 
    best_chain = np.argmax(lnprob)
    poor_chains = np.where(lnprob < np.percentile(lnprob, 33))
    for ix in poor_chains:
        pos[ix] = pos[best_chain]
    
    #Reset and go again!
    sampler.reset()
    sampler.run_mcmc(pos, n_chain)
    
    #Use plt.hist or even http://corner.readthedocs.io/en/latest/
    #to examine the outputs:
    #sampler.chain
    sampler.flatchain #(if you're feeling lazy)
    #e.g. 
    plt.hist(sampler.flatchain[:,0])
    plt.show()
