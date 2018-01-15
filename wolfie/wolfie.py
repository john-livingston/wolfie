import numpy as np
import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
import pkg_resources

_FP = pkg_resources.resource_filename(__name__, 'R/posterior_samples.savr')
robjects.r.load(_FP)

_FP = pkg_resources.resource_filename(__name__, 'R/calc_mass_postpred.R')
robjects.r.source(_FP)

trdepth2rad = robjects.r['trdepth2rad']
massguess_individpl = robjects.r['massguess_individpl']
postsamp_eqn2_baseline = rpy2.robjects.r['postsamp_eqn2_baseline']


def df_from_params(rstar, urstar, rprs, urprs, numsamples=10000):
    
    """
    rstar : stellar radius in solar units
    urstar : uncertainty in rstar
    rprs : the ratio Rp/Rstar
    urprs : the uncertainty in rprs
    numsamples : the number of samples to use for mass prediction
    """

    stelrad = np.random.randn(numsamples) * urstar + rstar
    # can use stellar radius samples directly instead if available (i.e. from isochrones)

    ratio = np.random.randn(numsamples) * urprs + rprs
    # can use Rp/Rstar samples directly instead if available

    df = df_from_samples(stelrad, ratio, numsamples=numsamples)

    return df


def df_from_samples(stelrad, ratio, numsamples=10000):

    """
    stelrad : samples of the stellar radius in solar units
    ratio : samples of the ratio Rp/Rstar
    numsamples : the number of samples to use for mass prediction
    """

    planrad = trdepth2rad(stelrad, ratio, numsamp=numsamples, ratioisdepth=False)
    # calculates the planet radius distribution given samples of stellar radius and Rp/Rs

    postpred = massguess_individpl(postsamp_eqn2_baseline, numsamples, rad=planrad, raderr=0)
    # calculates the planet mass distribution given the planet radius distribution

    radii = np.array(postpred[0])
    masses = np.array(postpred[1])
    isrocky = np.array(postpred[2]).astype(bool)
    df = pd.DataFrame(dict(radii=radii, masses=masses, isrocky=isrocky))

    return df


if __name__ == '__main__':

    import sys

    rstar, urstar = map(float, sys.argv[1:3])
    rprs, urprs = map(float, sys.argv[3:5])
    df = df_from_params(rstar, urstar, rprs, urprs)

    print(df.describe())
