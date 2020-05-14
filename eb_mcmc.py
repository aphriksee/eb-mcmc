import sys
import os
import numpy as np
import emcee
from schwimmbad import MPIPool
 
# Try to set the PHOEBE to run with single job (not parallel)
input_environ = dict(os.environ)
try:
  del os.environ['PMI_SIZE']
except:
  print("Can't set the single job")
import phoebe
os.environ.clear()
os.environ.update(input_environ)


 
