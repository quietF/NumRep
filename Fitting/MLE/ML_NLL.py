import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


def NLL(params, t):
    """
    :param params: [fraction of first component, lifetime of 1st component, lifetime of 2nd component]
    :param t: time array
    :return: value of the Negative Log-Likelihood function with given parameters.
    """
    frac1 = params[0]
    tau1 = params[1]
    tau2 = params[2]
    ML_log = np.log(frac1 * np.exp(-t / tau1) / tau1 + (1.0 - frac1) * np.exp(-t / tau2) / tau2)
    nll = - np.sum(ML_log)
    return nll


def getError(good_params, minNLL, observed_times, parameter_index):  # i is good_params index to get the error
    """
    :param good_params: best-fit parameters (obtained from getParams(observed_times).x)
    :param minNLL: minimised NLL (obtained from getParams(observed_times).fun)
    :param observed_times: array of "DecayTimesData.txt"
    :param parameter_index: 0 for fraction of 1st component, 1 for lifetime of 1st component, 2 for lifetime of 2nd component
    :return: error for the required parameter
    """
    N = 100
    good_param = good_params[parameter_index]
    params = np.copy(good_params)
    closest_difference = 1.
    error = 0

    for p in range(N):
        params[parameter_index] = good_param * (0.5 + p / N)

        if parameter_index == 0 and params[parameter_index] < 1. and params[
            parameter_index] > 0.:  # varying fraction of first component
            difference = np.abs(NLL(params, observed_times) - minNLL)
            if np.abs(0.5 - difference) < closest_difference:
                closest_difference = np.abs(0.5 - difference)
                error = np.abs(good_param - params[parameter_index])
        elif params[parameter_index] > 0.:  # varying lifetime of first component if i == 1 or of second if i == 2.
            difference = np.abs(NLL(params, observed_times) - minNLL)
            if np.abs(0.5 - difference) < closest_difference:
                closest_difference = np.abs(0.5 - difference)
                error = np.abs(good_param - params[parameter_index])

    return error


def get_variation(good_params, minNLL, observed_times, parameter_index):
    """
    :param good_params: best-fit parameters (obtained from getParams(observed_times).x)
    :param minNLL: minimised NLL (obtained from getParams(observed_times).fun)
    :param observed_times: array of "DecayTimesData.txt"
    :param parameter_index: 0 for fraction of 1st component, 1 for lifetime of 1st component, 2 for lifetime of 2nd component
    :return: plot of the NLL for the required parameter's +- 3sigma variation from its mean.
    """
    param_error = getError(good_params, minNLL, observed_times, parameter_index)
    params = np.copy(good_params)
    N = 100
    nll = np.zeros(N)
    par = np.full(N, (params[parameter_index] - 3. * param_error)) + 2. * 3. * np.arange(N) * param_error / (N - 1.)

    for p in range(N):
        params[parameter_index] = par[p]
        nll[p] = NLL(params, observed_times)

    plot_info = [[r'Negative Log-Likelihood with Varying f', r'Negative Log-Likelihood with Varying $\tau_1$',
                  r'Negative Log-Likelihood with Varying $\tau_2$'], [r'f', r'$\tau_1$', r'$\tau_2$'],
                 ["img/fraction_varyingNLL.png", "img/tau1_varyingNLL.png", "img/tau2_varyingNLL.png"]]

    plt.title(plot_info[0][parameter_index])
    plt.xlabel(plot_info[1][parameter_index])
    plt.ylabel("Negative Log-Likelihood")
    plt.plot(par, nll, 'r', np.full(N, good_params[parameter_index]), nll, 'b')
    plt.savefig(plot_info[2][parameter_index])
    plt.close()


def getParams(observed_times):
    """
    :param observed_times: array of decay times
    :return: scipy.optimize.minimize result (res.x returns the best fit parameters)
    """
    init_params = np.array([0., 0.1, 0.1])  # [f, tau1, tau2]
    bound = ((0., 1.), (0.01, None), (0.01, None))

    res = optimize.minimize(NLL, init_params, method='SLSQP', args=(observed_times,), bounds=bound)
    return res


# fn = str(input("Input datafile name: "))
input_file = "in/DecayTimesData.txt"

print(input_file)
t_array = np.loadtxt(input_file)

minimizer = getParams(t_array)

params = minimizer.x
minNLL = minimizer.fun

error_f = getError(params, minNLL, t_array, 0)
error_tau1 = getError(params, minNLL, t_array, 1)
error_tau2 = getError(params, minNLL, t_array, 2)
print("observed best-fit parameters: {0} {1} {2}".format(params[0], params[1], params[2]))
print("observed best-fit parameters error: {0} {1} {2}".format(error_f, error_tau1, error_tau2))

"""
Produce plots of variation of each parameter
"""

get_variation(params, minNLL, t_array, 0)
get_variation(params, minNLL, t_array, 1)
get_variation(params, minNLL, t_array, 2)
