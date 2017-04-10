import MCsim
import matplotlib.pyplot as plt
import numpy as np

bounds = [0.0, 7.0]
input_file = "in/DecayTimesData.txt"
mc = MCsim.MonteCarlo(input_file, bounds)

test_time_array = mc.getRandomDistribution(10000)
np.savetxt("out/DecayTimesSimulation.txt", test_time_array)

mc_params = mc.runMonteCarlo(500, 10000) # run 500 MC simulations each with 10000 decay times.
np.savetxt("out/ParametersSimulation.txt", np.transpose(mc_params))

simulated_params = [np.average(mc.f_simulated), np.average(mc.tau1_simulated), np.average(mc.tau2_simulated)]
jacknife_errors = [mc.getJacknife(0), mc.getJacknife(1), mc.getJacknife(2)]
std_errors = [np.std(mc.f_simulated), np.std(mc.tau1_simulated), np.std(mc.tau2_simulated)]

print("simulated best-fit parameters: {0} {1} {2}".format(simulated_params[0],
                                                          simulated_params[1], simulated_params[2]))
print("simulated best-fit parameters Jacknife error: {0} {1} {2}".format(jacknife_errors[0],
                                                                         jacknife_errors[1], jacknife_errors[2]))
print("simulated best-fit parameters standard deviation error: {0} {1} {2}".format(std_errors[0],
                                                                                   std_errors[1], std_errors[2]))


plt.xlabel("Fraction of 1st Component")
plt.hist(mc.f_simulated, bins=100)
plt.savefig("img/fraction.png")
plt.close()

plt.xlabel("Lifetime of 1st Component")
plt.hist(mc.tau1_simulated, bins=100)
plt.savefig("img/tau1.png")
plt.close()

plt.xlabel("Lifetime of 2nd Component")
plt.hist(mc.tau2_simulated, bins=100)
plt.savefig("img/tau2.png")
plt.close()