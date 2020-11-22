import numpy as np

class XGC_f0_diag:
	def __init__(self, xgcexp):
		self.f0_nmu = xgcexp.f0mesh.f0_nmu
		self.f0_nvp = xgcexp.f0mesh.f0_nvp
		self.f0_smu_max = xgcexp.f0mesh.f0_smu_max
		self.f0_dsmu = xgcexp.f0mesh.f0_dsmu
		self.f0_T_ev = xgcexp.f0mesh.f0_T_ev
		self.f0_grid_vol_vonly = xgcexp.f0mesh.f0_grid_vol_vonly
		self.f0_dvp = xgcexp.f0mesh.f0_dvp    
		self.f0_nnodes = xgcexp.mesh.nnodes

	def f0_diag(self, isp, f0_f):
		nmu = self.f0_nmu + 1
		f0_nvp = self.f0_nvp
		nvp = f0_nvp * 2 + 1
		n_nodes = self.f0_nnodes
		assert(f0_f.shape[0] == n_nodes)
		assert(f0_f.shape[1] == nmu)
		assert(f0_f.shape[2] >= nvp)
		smu_max = self.f0_smu_max
		dsmu = self.f0_dsmu
		T_ev = self.f0_T_ev[isp]
		grid_vol_vonly = self.f0_grid_vol_vonly[isp]
		dvp = self.f0_dvp

		ptl_e_mass_au = 2E-2
		ptl_mass_au = 2E0
		sml_prot_mass = 1.6720E-27
		ptl_mass_ = [ptl_e_mass_au*sml_prot_mass, ptl_mass_au*sml_prot_mass]
		ptl_mass = ptl_mass_[isp]

		electron_charge = 1.6022E-19 
		# dv_perp
		mu_vol = np.ones(nmu)
		mu_vol[0] = 0.5
		mu_vol[-1] = 0.5
		# dv_para
		vp_vol = np.ones(nvp)
		vp_vol[0] = 0.5
		vp_vol[-1] = 0.5
		# dv_perp dv_para
		dv_perp_dv_para = np.outer(mu_vol, vp_vol)
		# intermediate
		vth = np.sqrt(T_ev * (electron_charge / ptl_mass))
		vp = (np.arange(0, nvp, dtype=np.float64) - f0_nvp) * dvp
		vp = np.tile(vp, (nmu, 1))
		mu = np.arange(nmu, dtype=np.float64)*dsmu
		mu = np.tile(mu.reshape(mu.size, 1), (1, nvp))
		# init
		density = np.zeros([n_nodes])
		u_para = np.zeros([n_nodes])
		T_perp = np.zeros([n_nodes])
		T_para = np.zeros([n_nodes])
		# compute
		for i in range(0, n_nodes):
			node_vol = grid_vol_vonly[i] * dv_perp_dv_para
			v_perp = mu * vth[i]
			v_para = vp * vth[i]
			# f * dv_perp dv_para
			f_dv_perp_dv_para = f0_f[i] * node_vol
			# density: Int(f dv_perp dv_para)
			density[i] = np.sum(f_dv_perp_dv_para)
			# u_para: Int(v_para f dv_perp dv_para)
			u_para[i] = np.sum(v_para * f_dv_perp_dv_para) / density[i]
			# T_perp: Int(1/2 m v_perp^2 f dv_perp dv_para)
			T_perp[i] = np.sum(0.5 * ptl_mass * v_perp**2 * f_dv_perp_dv_para) / density[i] / electron_charge
			# T_para: Int(1/2 m (v_para - u_para)^2 f dv_perp dv_para)
			T_para[i] = 2.0 * np.sum(0.5 * ptl_mass * (v_para - u_para[i])**2 * f_dv_perp_dv_para) / density[i] / electron_charge
		return density, u_para, T_perp, T_para

