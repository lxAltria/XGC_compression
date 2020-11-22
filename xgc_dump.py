import numpy as np
import sys
sys.path.append('/Users/x0o/github/ADIOS2_ext/ADIOS2_python3/install/lib/python3.8/site-packages')
import adios2 as ad2

#from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import os
import subprocess

def compute_diff(name, x, x_):
    max_diff = np.max(np.abs(x - x_))
    vrange = np.max(x) - np.min(x)
    print("{}: abs diff = {}, relative diff = {}".format(name, max_diff, max_diff/vrange))

# Output filename
qoi_file = "QoI.npz"
data_file = "xgc_f64.dat"
## module for xgc experiment: https://github.com/jychoi-hpc/xgc4py
import xgc4py

with ad2.open('xgc.f0_debug.00702.10.bp', 'r') as f:
	i_f = f.read('i_f')
	n0_stored = f.read('n0')
	T0_stored = f.read('T0') 

xgcexp = xgc4py.XGC()

import f0_diag_test
xgc = f0_diag_test.XGC_f0_diag(xgcexp)

n_phi, n_dv_perp, n_nodes, n_dv_para = i_f.shape
print(i_f.shape)
density = np.zeros([n_phi, n_nodes])
u_para = np.zeros([n_phi, n_nodes])
T_perp = np.zeros([n_phi, n_nodes])
T_para = np.zeros([n_phi, n_nodes])
for i in range(n_phi):
	density[i], u_para[i], T_perp[i], T_para[i] = xgc.f0_diag(isp=1, f0_f=np.moveaxis(i_f[i], 0, 1))

n0 = density.copy()
T0 = (2.0*T_perp + T_para)/3.0
compute_diff("n0", n0, n0_stored)
compute_diff("n0", T0, T0_stored)
n0_avg, T0_avg = xgcexp.f0_avg_diag(0, n_nodes, n0, T0)
print("Store computed quantities...")
np.savez(qoi_file, density, u_para, T_perp, T_para, n0_avg, T0_avg)
print("Done... QoI written to {}...".format(qoi_file))
print("Reorder and store data...")
print(i_f.shape)
i_f = np.moveaxis(i_f, 1, 2)
i_f = np.moveaxis(i_f, 0, 1)
print(i_f.shape)
i_f.tofile(data_file)
print("Done... Data written to {}...".format(data_file))

