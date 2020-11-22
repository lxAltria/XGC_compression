import numpy as np
import sys
import os

logfile = sys.argv[1]
outfile = 'ratio_distortion_{}.pdf'.format(logfile)

qois = ['density', 'u_para', 'T_perp', 'T_para', 'n0_avg', 'T0_avg']

print("Extracting ratios...")
os.system("sh collect_ratio.sh {} > ratio.txt".format(logfile))
ratio = np.loadtxt("ratio.txt")
err = np.zeros([len(qois), len(ratio)])
print("Extracting error of QoI...")
i = 0
for qoi in qois:
	os.system("sh collect_error.sh {} {} > error.txt".format(logfile, qoi, qoi))
	err[i] = np.loadtxt("error.txt")
	i = i + 1

print("Plotting...")
from matplotlib import pyplot as plt
styles=['y-*', 'b-^', 'g--s','c-.+', 'r:x', 'm-d']
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(12,8))
ax=[axs[0,0], axs[0,1], axs[1,0], axs[1,1], axs[2,0], axs[2,1]]
i = 0
for qoi in qois:
	p, = ax[i].plot(ratio, err[i], styles[i], label='{}'.format(qoi))
	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax[i].set_ylabel('L-inf error')
	ax[i].set_yticks([1e-1, 1e-2, 1e-3, 1e-4])
	ax[i].set_yscale('log')
	ax[i].grid(which='major', axis='y')
	ax[i].set_title(qoi)
	ax[i].set_xlabel('Compression ratio')
	ax[i].legend(loc='lower right')
	i = i + 1

plt.tight_layout()
plt.savefig(outfile)
print("Figure saved to {}.".format(outfile))
