###############################################################
#
# Constant pressure or Constant-volume reactor,
# adiabatic kinetics simulation.
#
###############################################################

#import :

import sys
import csv
import cantera
from cantera import *
import numpy as np


#################################################################
# Prepare your run
#################################################################
#Mechanism used for the process
cti = Solution('gri30.cti')
air = Solution('air.xml')

#Gaseous fuel species
fuel_species = 'CH4'

#Number of species in the.cti file.
m = cti.n_species

#Find fuel, nitrogen, and oxygen indices
fuel_species = 'CH4'
ifuel = cti.species_index(fuel_species)
io2 = cti.species_index('O2')
in2 = cti.species_index('N2')

if ifuel < 0:
    raise Exception("fuel species " + fuel_species + " not present!")

if cti.n_atoms(fuel_species, 'O') > 0 or cti.n_atoms(fuel_species, 'N') > 0:
    raise Exception("Error: only hydrocarbon fuels are supported.")

#################
#Enter general parameters

# Stoechiometry
print("")
print("-------------------------------------------------------- ")
print("    THERMO PROPERTIES: ")
print("-------------------------------------------------------- ")
print("")
phi = float(input('Enter Stoichiometric ratio phi : '))
print("")

# Air composition
air_N2_O2_ratio = 3.76
stoich_O2 = cti.n_atoms(fuel_species, 'C') + 0.25 * cti.n_atoms(fuel_species, 'H')

# Mass fraction vector
x = np.zeros(m, dtype='d')
x[ifuel] = phi
x[io2] = stoich_O2
x[in2] = stoich_O2 * air_N2_O2_ratio

# Specify initial pressures and temperature of the reactor
Ti = float(input('Enter temperature (in kelvin) : '))
Pi = float(input('Enter pressure (in bar) : ')) * 1e5  # Pascal

# Set initial conditions
cti.TPX = Ti, Pi, x

#################################################################
# Program starts here
#################################################################
# Create the batch reactor
r = IdealGasReactor(cti)

# Specify the conditions: Pressure or Volume constant
print("--------------------------------------------------- ")
print("    Equilibrium conditions: ")
print("--------------------------------------------------- ")
print("")
print("For a constant volume equilibrium, enter :      UV ")
print("For a constant pressure equilibrium, enter :    HP ")
print("")
cond = input('Specify the equilibrium condition : ')
print("")
while cond != 'HP' and cond != 'UV':
    print("You must choose between UV and HP !  ")
    cond = input('Specify the equilibrium condition : ')

# Particular case of a constant-pressure reactor
if cond == 'HP':
    # Define a wall between the reactor and the environment, and
    # make it flexible, so that the pressure in the reactor is held
    # at the environment pressure.
    env = Reservoir(air)
    w = Wall(r, env)
    w.expansion_rate_coeff = 1.0e6   # set expansion parameter. dV/dt = KA(P_1 - P_2)
    w.area = 1.0       # set wall area

# Now create a reactor network consisting of the single batch reactor
# Reason: the only way to advance reactors in time is through a network
sim = ReactorNet([r])

#################
# Computational properties: we're going to advance the network in time

print("")
print("-------------------------------------------------------- ")
print("    COMPUTATIONAL PROPERTIES: ")
print("-------------------------------------------------------- ")
print("")

# Initial simulation time
time = 4.0e-1

# Specify the number of time steps
nt = int(input('Enter number of time steps: '))

# Specify the time step
dtms = int(input('Enter the time step (in ms): '))
dt = dtms * 1.0e-3  # s

#################
# Run the simulation

# Parameters
tim = np.zeros(nt, dtype='d')
temp = np.zeros(nt, dtype='d')
press = np.zeros(nt, dtype='d')
mfrac = np.zeros([nt, m], dtype='d')

# Loop for nt time steps of dt seconds.
print('time [s] ,   T [K] ,   p [Pa] ,   u [J/kg]')
for n in range(nt):
    time += dt
    sim.advance(time)
    tim[n] = time
    temp[n] = r.T
    press[n] = r.thermo.P
    for i in range(m):
        mfrac[n, i] = r.thermo[cti.species_name(i)].Y
    print('%10.3e %10.3f %10.3f %14.6e' % (sim.time, r.T,
                                           r.thermo.P, r.thermo.h))

#################################################################
# Save your results if needed
#################################################################
# write output CSV file for importing into Excel
if cond == 'HP':
    csvfile = 'Reactor_HP.csv'
elif cond == 'UV':
    csvfile = 'Reactor_UV.csv'

csv_file = csvfile
with open(csv_file, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Time', 'Temperature', 'Pressure'] + cti.species_names)
    for n in range(nt):
        writer.writerow([tim[n], temp[n], press[n]] + list(mfrac[n, :]))
print('output written to ' + csvfile)

#################################################################
# Plot your results
#################################################################
# plot the results if matplotlib is installed.
# see http://matplotlib.sourceforge.net to get it
args = sys.argv
if len(args) > 1 and args[1] == '-plot':
    import matplotlib.pyplot as plt

    plt.clf()
    plt.subplot(2, 2, 1)
    plt.plot(tim, temp[:])
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (K)')
    plt.subplot(2, 2, 2)
    plt.plot(tim, mfrac[:, cti.species_index('OH')])
    plt.xlabel('Time (s)')
    plt.ylabel('OH Mass Fraction')
    plt.subplot(2, 2, 3)
    plt.plot(tim, mfrac[:, cti.species_index('H')])
    plt.xlabel('Time (s)')
    plt.ylabel('H Mass Fraction')
    plt.subplot(2, 2, 4)
    plt.plot(tim, mfrac[:, cti.species_index('H2')])
    plt.xlabel('Time (s)')
    plt.ylabel('H2 Mass Fraction')
    plt.show()
else:
    print("To view a plot of these results, run this script with the option -plot")
