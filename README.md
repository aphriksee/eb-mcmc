# eb-mcmc
Use PHOEBE and MCMC technique to estimate the physical parameters of eclipsing binary systems

## Running an example code

```
mpiexec -n 56 python example.py
```

### Prerequisites
* PHOEBE
* emcee
* schwimmbad
* corner

### Feature
- Model the light curve (synthetic line) using the PHOEBE
- Use MPI and EMCEE to parallel run and find the posterior distribution
- Plot the results using the CORNER package

### Link (with tested version)
* PHOEBE, ver. 2.2.1, phoebe-project.org
* emcee, ver. 3.0.2,  github.com/dfm/emcee
* corner, ver. 2.0.1, github.com/dfm/corner.py
* schwimmbad, ver. 0.3.1
* etc. mpich/mpi4py
