# Python/Bash script for evaluating QoI perservation of XGC data with MGARD compression

Require XGC output in ADIOS format:
xgc.equil.bp/             xgc.f0_debug.00702.10.bp/ xgc.mesh.bp/              
xgc.f0.mesh.bp/           xgc.fluxavg.bp/
fort.input.used	 

Require xgc4py: https://github.com/jychoi-hpc/xgc4py

# Usage
sh run_mgard_batch.sh<br/>
python3 plot_err.py mgard_2.8284.log<br/>


