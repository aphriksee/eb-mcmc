# Fitting Phoebe with emcee
# A. Phriksee
# Ver. 1.0, 14/05/2020
 
import os
os.environ["OMP_NUM_THREADS"] = "1"

# Import Extension
import sys
import numpy as np
import emcee
import time
from schwimmbad import MPIPool

# Try to force the PHOEBE to run with single core in each value
temp_environ = dict(os.environ)
del os.environ['PMI_SIZE']
import phoebe
os.environ.clear()
os.environ.update(temp_environ)

# Input data
data = np.loadtxt("mock_data.dat")
JD       = data[:, 0]
flux     = data[:, 1]
err_gflux = data[:, 2]

# Setting BC
pos_lim_min = np.array([0.15, 0.10, 35000.0, 1500.0, 1.0])
pos_lim_max = np.array([0.25, 0.22, 48000.0, 4000.0, 10.0])

# Setting emcee
ndim = len(pos_lim_min)
nwalkers = 10 * ndim
burnin = 1000

# Set the initial binary model
b = phoebe.default_binary()
b.filter()
b.add_dataset('lc', times=JD, fluxes=flux, dataset='lc01')
b.set_value('ld_mode', component='primary', dataset='lc01', value='manual')
b.set_value('ld_mode', component='secondary', dataset='lc01', value='manual')
b.set_value('ld_func', component='primary', dataset='lc01', value='logarithmic')
b.set_value('ld_func', component='secondary', dataset='lc01', value='logarithmic')
b.set_value_all('ld_mode_bol', value='manual')
b.set_value('atm@primary@phoebe01@phoebe@compute', value='blackbody')
b.set_value('atm@secondary@phoebe01@phoebe@compute', value='blackbody')
b.set_value('ecc', component='binary', value = ecc)

# Set model and create light curve
def LC_sim_r(params_fit):
	(r1, r2, T1, T2, pblum) = params_fit
	b_model = b
	b_model.set_value('requiv', component='primary', value=r1)
	b_model.set_value('requiv', component='secondary', value=r2)
	b_model.set_value('teff', component='primary', value = T1)
	b_model.set_value('teff', component='secondary', value = T2)
	b_model.set_value('period', component='binary', value = P)
	b_model.set_value('pblum', component='primary', value = pblum*np.pi)
	
	# Compute a model
	b_model.run_compute()
	
	lc_model = b_model.get_value('fluxes@lc@model')
	del b_model
	return lc_model

# Set BC for the prior parameters
def lnprior(theta):
        if ((pos_lim_min<theta).all()) & ((theta<pos_lim_max).all()):
                return 0.0
        return -np.inf

# Log-likelihood function
def lnlike(theta):
	try:
		LC_model = LC_sim(theta)
		LC_model_r = LC_sim_r(theta)
		sigma2 = err_flux**2.0
		chisq = np.sum((flux - LC_model)**2.0 / sigma2)
	except:
		chisq = np.inf
	return -0.5 * chisq

# Log-likelihood prob
def lnprob(theta):
	lp = lnprior(theta)
	if not np.isfinite(lp):
		return -np.inf
	return lp + lnlike(theta)

# Main program
def main_fit():
	pool = MPIPool()
	if not pool.is_master():
		pool.wait()
		sys.exit(0)
	psize = pos_lim_max-pos_lim_min
	p0   = [pos_lim_min + psize*np.random.rand(ndim) for i in range(nwalkers)]
	sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, pool=pool)
	pool.close()

# Call main program
if __name__ == "__main__":
	main_fit()
