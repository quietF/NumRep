import numpy as np
from ML_NLL import getParams

class MonteCarlo:

    def __init__(self, time_file, boundary):
        observed_times = np.loadtxt(time_file)
        params = getParams(observed_times).x
        self.f = params[0]
        self.tau1 = params[1]
        self.tau2 = params[2]

        self.t_min = boundary[0]
        self.t_max = boundary[1]
        t_step = (self.t_max - self.t_min) / 1000.
        times = np.arange(self.t_min, self.t_max, t_step)
        probabilities = np.zeros(len(times))
        probabilities[:] = self.evaluateDistribution(times[:])
        self.probability_max = np.max(probabilities)

    def evaluateDistribution(self, time):
        return self.f * np.exp(-time / self.tau1) / self.tau1 + (1.0-self.f) * np.exp(-time / self.tau2) / self.tau2

    def getRandom(self):
        randomNumber = self.t_min + (self.t_max - self.t_min) * np.random.rand(1)
        y1 = self.evaluateDistribution(randomNumber)
        y2 = self.probability_max * np.random.rand(1)

        if y2 < y1:
            return randomNumber
        else:
            return self.getRandom()

    def getRandomDistribution(self, N):
        NrandomNumber = np.zeros(N)
        for i in range(N):
            NrandomNumber[i] = self.getRandom()
        return NrandomNumber

    def runOneSimulation(self, N):
        time_histogram = self.getRandomDistribution(N)
        params_simulation = getParams(time_histogram).x
        return params_simulation

    def runMonteCarlo(self, nSimulations, nPoints):
        params_simulated = np.zeros((3, nSimulations))
        for i in range(nSimulations):
            params_simulation = self.runOneSimulation(N=nPoints)
            while np.isnan(params_simulation).any() or (params_simulation == 0.).any() or \
                            params_simulation[0] > 0.9 or params_simulation[0] < 0.1:
                params_simulation = self.runOneSimulation(N=nPoints)

            params_simulated[0][i] = params_simulation[0]
            params_simulated[1][i] = params_simulation[1]
            params_simulated[2][i] = params_simulation[2]

        normal_f = [np.average(params_simulated[0]), np.std(params_simulated[0])]
        normal_tau1 = [np.average(params_simulated[1]), np.std(params_simulated[1])]
        normal_tau2 = [np.average(params_simulated[2]), np.std(params_simulated[2])]

        self.f_simulated = []
        self.tau1_simulated = []
        self.tau2_simulated = []

        for i in range(nSimulations):
            if np.abs(params_simulated[0][i] - normal_f[0]) < 5 * normal_f[1] and \
                            np.abs(params_simulated[1][i] - normal_tau1[0]) < 5 * normal_tau1[1] and \
                            np.abs(params_simulated[2][i] - normal_tau2[0]) < 5 * normal_tau2[1]:
                self.f_simulated = np.append(self.f_simulated, params_simulated[0][i])
                self.tau1_simulated = np.append(self.tau1_simulated, params_simulated[1][i])
                self.tau2_simulated = np.append(self.tau2_simulated, params_simulated[2][i])

        np.savetxt("out/fraction.txt", self.f_simulated)
        np.savetxt("out/tau1.txt", self.tau1_simulated)
        np.savetxt("out/tau2.txt", self.tau2_simulated)

        return [self.f_simulated, self.tau1_simulated, self.tau2_simulated]

    def getJacknife(self, parameter_index):
        """
        :param parameter_index: 0 for fraction of 1st component, 1 for lifetime of 1st component, 2 for lifetime of 2nd component
        :return: jacknife error
        """
        if parameter_index == 0:
            parameter_array_copy = np.copy(self.f_simulated)
        elif parameter_index == 1:
            parameter_array_copy = np.copy(self.tau1_simulated)
        elif parameter_index == 2:
            parameter_array_copy = np.copy(self.tau2_simulated)
        else:
            return 0

        parameter_real = np.mean(parameter_array_copy)

        parameter_error = 0.
        parameter_jacknife = np.zeros((len(parameter_array_copy) - 1, len(parameter_array_copy) - 1))
        for i in range(len(parameter_array_copy) - 1):
            parameter_jacknife[i] = np.delete(parameter_array_copy, i)
            parameter_error += (parameter_real - np.average(parameter_jacknife[i])) ** 2.

        return np.sqrt(parameter_error)