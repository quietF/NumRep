import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

def NLL(params, t):
	frac1 = params[0]
	tau1 = params[1]
	tau2 = params[2]
	ML_log = np.log(frac1 * np.exp(-t/tau1) / tau1 + (1.0-frac1) * np.exp(-t/tau2) / tau2)
	nll = - np.sum(ML_log)
	return nll
	
def error(good_params, minNLL, t, i): # i is good_params index to get the error
	N=100
	good_param = good_params[i]
	params = np.copy(good_params)
	half_diff = 1.
	error = 0
	
	for p in range(N):
		params[i] = good_param * (0.5 + p/N)

		if i == 0 and params[i] < 1. and params[i] > 0.:
			diff = np.abs(NLL(params, t) - minNLL)
			if np.abs(0.5 - diff) < half_diff:
				half_diff = np.abs(0.5 - diff)
				error = np.abs(good_param-params[i])
		elif params[i] > 0.:
			diff = np.abs(NLL(params, t) - minNLL)
			if np.abs(0.5 - diff) < half_diff:
				half_diff = np.abs(0.5 - diff)
				error = np.abs(good_param-params[i])
				
	return error
	
def get_variation(good_params, minNLL, t, i):
	param_error = error(good_params, minNLL, t, i)
	params = np.copy(good_params)
	N = 100
	nll = np.zeros(N)
	par = np.full(N, (params[i]-3. * param_error)) + 2. * 3. * np.arange(N) * param_error / (N-1.)
	
	for p in range(N):
		params[i] = par[p]
		nll[p] = NLL(params, t)
		
	plt.plot(par, nll, 'r', np.full(N, good_params[i]), nll, 'b')
	plt.show()
			

#fn = str(input("Input datafile name: "))
fn = "DecayTimesData.txt"

print(fn)
t_array = np.loadtxt(fn)

#print(NLL(t_array, [0.5, 1.2, 1.9]))

init_params = np.array([0., 0.1, 0.1]) # [f, tau1, tau2]
bound = ((0., 1.), (0.01, None), (0.01, None))

res = optimize.minimize(NLL, init_params, method='SLSQP', args=(t_array,), bounds=bound)

print(res)

params = res.x
minNLL = res.fun

error_f = error(params, minNLL, t_array, 0)
error_tau1 = error(params, minNLL, t_array, 1)
error_tau2 = error(params, minNLL, t_array, 2)
print("{0} {1} {2}".format(params[0]+3.*error_f, params[1]+3.*error_tau1, params[2]+3.*error_tau2))

get_variation(params, minNLL, t_array, 0)
get_variation(params, minNLL, t_array, 1)
get_variation(params, minNLL, t_array, 2)
