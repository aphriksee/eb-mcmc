# Eclipsing Binaries - MCMC
Use PHOEBE and MCMC technique to estimate the physical parameters of eclipsing binary systems

## Running an example code
Write a simple code for the MPI job
```
mpiexec -n 32 python example.py
```

### Feature
- Model the light curve (synthetic line) using the PHOEBE
- Use MPI and EMCEE to parallel run and find the posterior distribution
- Plot the results using the CORNER package


### Example : 
Let consider an ecclipsing bianry system, we would like to extract the physical parameters :
Radius, Temperature, Period, t0, semi-major-axis, mass ration and inclination.

![Priliminary results of Posterior distributions from emcee](example/results.png)
*we will public the full results soon!


### Speed
Try to run an exmaple code with vary number of CPU cores

(Fixed Nwalker = 10 * Ndim, and 20 steps)

![Cores vs Time](test/speed.png)

### Prerequisites (tested version)
* PHOEBE, ver. 2.2.1, phoebe-project.org
* emcee, ver. 3.0.2,  github.com/dfm/emcee
* schwimmbad, ver. 0.3.1
* corner, ver. 2.0.1, github.com/dfm/corner.py
* etc. mpich/mpi4py
