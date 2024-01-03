###############################################################
#
# Constant pressure or Constant-volume reactor, 
#             adiabatic kinetics simulation.
#              
###############################################################

#import :

import sys

from Cantera import *
from Cantera.Reactor import *
#from Cantera.Func import *
#from Cantera import rxnpath
from matplotlib.pylab import *


#################################################################
# Prepare your run
#################################################################
#Mechanism used for the process
cti = importPhase('gri30.cti')

#Gaseous fuel species
fuel_species = 'CH4'

#Number of species in the.cti file.
m=cti.nSpecies()

#Find fuel, nitrogen, and oxygen indices
ifuel, io2, in2 = cti.speciesIndex([fuel_species, 'O2', 'N2'])

if ifuel < 0:
    raise "fuel species "+fuel_species+" not present!"

if cti.nAtoms(fuel_species,'O') > 0 or  cti.nAtoms(fuel_species,'N') > 0:
    raise "Error: only hydrocarbon fuels are supported."

#################
#Enter general parameters

	#Stoechiometry
print ""
print "-------------------------------------------------------- "
print "    THERMO PROPERTIES: "
print "-------------------------------------------------------- "
print ""
phi        = input('Enter Stoichiometric ratio phi : ')
phi        = float(phi)
print ""

		#Air composition
air_N2_O2_ratio = 3.76   
stoich_O2 = cti.nAtoms(fuel_species,'C') + 0.25*cti.nAtoms(fuel_species,'H')

		#Mass fraction vector
x = zeros(m,'d')
x[ifuel] = phi
x[io2] = stoich_O2
x[in2] = stoich_O2*air_N2_O2_ratio


	# Specify intial pressures and temperature of the reactor
Ti = input('Enter temperature (in kelvin) : ')
Ti = float(Ti)       # Kelvin

Pi = input('Enter pressure (in bar) : ')
Pi = float(Pi)*1e5         # Pascal


	#Set initial conditions
cti.set(T = Ti, P = Pi, X = x)


#################################################################
# Program starts here
#################################################################
#Create the batch reactor
r   = Reactor(cti)


#Specify the conditions: Pression or Volume constant
print "--------------------------------------------------- "
print "    Equilibirum conditions: "
print "--------------------------------------------------- "
print ""
print "For a constant volume equilibrium, enter :      UV "
print "For a constant pressure equilibrium, enter :    HP "
print ""
cond  = raw_input('Specify the equilibrium condition : ')
cond  = str(cond)
print ""
while cond != 'HP' and cond != 'UV':
     print "You must choose between UV and HP !  "
     cond  = raw_input('Specify the equilibrium condition : ')
     cond  = str(cond)

	#Particular case of a constant-pressure reactor
if cond == 'HP':
	# Define a wall between the reactor and the environment, and
	# make it flexible, so that the pressure in the reactor is held
	# at the environment pressure.
     env = Reservoir(Air())
     w = Wall(r,env)
     w.set(K = 1.0e6)   # set expansion parameter. dV/dt = KA(P_1 - P_2)
     w.set(A = 1.0)     # set wall area


# Now create a reactor network consisting of the single batch reactor
# Reason: the only way to advance reactors in time is through a network
sim = ReactorNet([r])

#################
#Computational properties: we're going to advance the network in time

print ""
print "-------------------------------------------------------- "
print "    COMPUTATIONAL PROPERTIES: "
print "-------------------------------------------------------- "
print ""

	# Initial simulation time
time = 0.0

	# Specify the number of time steps
nt        = input('Enter number of time steps: ')
nt        = int(nt)

	# Specify the time step
dtms	  = input('Enter the time step (in micro s): ')
dtms	  = int(dtms)

dt = dtms * 10e-6 #s

#################
#Run the simulation

	#parameters
tim = zeros(nt,'d')
temp = zeros(nt,'d')
press = zeros(nt,'d')
mfrac = zeros([nt,m],'d')

	#Loop for nt time steps of dt seconds. 
print 'time [s] ,   T [K] ,   p [Pa] ,   u [J/kg]'
for n in range(nt):
    time += dt
    sim.advance(time)
    tim[n] = time
    temp[n] = r.temperature()
    press[n] = r.pressure()
    for i in range(m):
        mfrac[n,i]=r.massFraction(i)
    print '%10.3e %10.3f %10.3f %14.6e' % (sim.time(), r.temperature(), 
                                           r.pressure(), r.intEnergy_mass())


#################################################################
# Save your results if needed
#################################################################
# write output CSV file for importing into Excel
if cond == 'HP':
     csvfile = 'Reactor_HP.csv'
elif cond == 'UV':
     csvfile = 'Reactor_UV.csv'

f = open(csvfile,'w')
writeCSV(f,['Time','Temp','Press.']+cti.speciesNames())
for n in range(nt):
    writeCSV(f,[tim[n], temp[n], press[n]]+list(mfrac[n,:]))
f.close()
print 'output written to '+csvfile


#################################################################
# Plot your results
#################################################################
# plot the results if matplotlib is installed.
# see http://matplotlib.sourceforge.net to get it
args = sys.argv
if len(args) > 1 and args[1] == '-plot':
        clf
        subplot(2,2,1)
        plot(tim,temp[:])
        xlabel('Time (s)');
        ylabel('Temperature (K)');
        subplot(2,2,2)
        plot(tim,mfrac[:,cti.speciesIndex('OH')])
        xlabel('Time (s)');
        ylabel('OH Mass Fraction');
        subplot(2,2,3)
        plot(tim,mfrac[:,cti.speciesIndex('H')]);
        xlabel('Time (s)');
        ylabel('H Mass Fraction');
        subplot(2,2,4)
        plot(tim,mfrac[:,cti.speciesIndex('H2')]);
        xlabel('Time (s)');
        ylabel('H2 Mass Fraction');
        show()
else:
    print """To view a plot of these results, run this script with the option -plot"""
