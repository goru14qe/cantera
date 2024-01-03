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
#Mechanisms used for the process
matrice_cas      = ['gri30','NAJM','VALORANI','grimechLuLaw19ana','sankaran']
type_plot = ['.','*','_','<','>','^','^','+','^']

	# Specify the number of time steps
nt        = 100000

	# Specify the time step
dtms	    = 1
dt = dtms * 1.e-6 #s

#Storage
nb_cas           = len(matrice_cas)
tim              = zeros(nt,'d')
temp_cas         = zeros(nt,'d')
dtemp_cas        = zeros(nt,'d')
nsp_cas          = []
Autoignition_cas = []
FinalTemp_cas    = []
pres_cas         = []
mfrac_cas        = []

 


fuel_species     = 'CH4'
air_N2_O2_ratio = 3.76

#################
#Enter general parameters
phi        = 0.5
Pi         = 1.e5       # Pascal
cond       = 'HP'     # Const P or Cons V
Tmin         = 0.65       # Kelvin
Tmax         = 0.85       # Kelvin
npoints     = 5
Ti = zeros(npoints,'d')
Ti2 = zeros(npoints,'d')

#Set initial conditions
for i, cas in enumerate(matrice_cas):
  print 'Cas ' + cas +' :\n'

	# Import the mechanism
  cti  = importPhase(cas + '.xml')
#  air  = importPhase('air.xml')
		#Number of species
  m                = cti.nSpecies()
  nsp_cas.append(m)
		#Find fuel, nitrogen, and oxygen indices
  ifuel, io2, in2  = cti.speciesIndex([fuel_species, 'O2', 'N2'])
		#Air composition
  stoich_O2        = cti.nAtoms(fuel_species,'C') + 0.25*cti.nAtoms(fuel_species,'H')

	#Initial mass fraction vector
  x_i              = zeros(m,'d')
  x_i[ifuel]       = phi
  x_i[io2]         = stoich_O2
  x_i[in2]         = stoich_O2*air_N2_O2_ratio

	# create some arrays to hold the data
  FinalTemp_cas.append(zeros(npoints,'d'))
  pres_cas.append(zeros(npoints,'d'))
  mfrac_cas.append(zeros([npoints,m],'d'))
  Autoignition_cas.append(zeros(npoints,'d'))

  for j in range(npoints):  
    Ti2[j]   = Tmin + (Tmax - Tmin)*j/(npoints - 1)
    Ti[j]   = 1000/Ti2[j]

	#Set gas state
    cti.set(T = Ti[j], P = Pi, X = x_i)
#   air.set(T=Ti, P = Pi)

#################################################################
# Program starts here
#################################################################
	#Create the batch reactor
    r   = ConstPressureReactor(cti)

	#Set condition
#  if cond == 'HP':
		# Define a wall between the reactor and the environment, and
		# make it flexible, so that the pressure in the reactor is held
		# at the environment pressure.
#    env = Reservoir(air)
#    w   = Wall(r,env)
#    w.set(K = 1.0e6)   # set expansion parameter. dV/dt = KA(P_1 - P_2)
#    w.set(A = 1.0)     # set wall area

	# Now create a reactor network consisting of the single batch reactor
    sim   = ReactorNet([r])

#################
	#Run the simulation
		# Initial simulation time
    time      = 0.0


		#Loop for nt time steps of dt seconds. 
#    print 'time [s] ,   T [K] ,   p [Pa] ,   u [J/kg]'
    for n in range(nt):
      time += dt
      sim.advance(time)
      tim[n]          = time
      temp_cas[n]  = r.temperature()
#      pres_cas[i][n]  = r.pressure()
#      for sp in range(m):
#          mfrac_cas[i][j][sp] = r.massFraction(j)
#      print '%10.3e %10.3f %10.3f %14.6e' % (tim[n], r.temperature(), 
#                                           r.pressure(), r.intEnergy_mass())
    for sp in range(m):
       mfrac_cas[i][j][sp] = r.massFraction(sp)


#################################################################
# Post processing
#################################################################
	# Get autoignition timing
    Dtmax = [0,0.0]
    for n in range(nt-1):
      dtemp_cas[n] = (temp_cas[n+1]-temp_cas[n])/dt
      if (dtemp_cas[n]>Dtmax[1]):
        Dtmax[0] = n
        Dtmax[1] = dtemp_cas[n] 
		# Local print
    Autoignition         = (tim[Dtmax[0]]+tim[Dtmax[0] + 1])/2.
#    print 'Autoignition time = ' + str(Autoignition)
		# Posterity
    Autoignition_cas[i][j] = Autoignition*1000  #ms
    FinalTemp_cas[i][j] = temp_cas[nt-1]


#################################################################
# Save your results if needed
#################################################################
# write output CSV file for importing into Excel
if cond == 'HP':
     csvfile = 'Phi'+ str(phi) +'_P'+str(Pi)+'_Trange_HP.csv'
elif cond == 'UV':
     csvfile = 'Phi'+ str(phi) +'_P'+str(Pi)+'_Trange_UV.csv'

f = open(csvfile,'w')
for i, cas in enumerate(matrice_cas):
	# Import the mechanism for the correct number of species
  cti  = importPhase(cas + '.xml')
  m    = cti.nSpecies()
  writeCSV(f,[cas])
  for j in range(npoints):
    writeCSV(f,['cas Ti = '] + [Ti[j]])
    writeCSV(f,['Auto ignition time','Final Temperature'] + cti.speciesNames())
    f.write('%10.3e %10.3f ' % (Autoignition_cas[i][j], FinalTemp_cas[i][j]))
    for sp in range(m):
      f.write('%10.6e ' % (mfrac_cas[i][j][sp]))
    f.write("\n")
  f.write("\n")
f.close()

print 'output written to '+csvfile


#################################################################
# Plot your results
#################################################################
# create plot
fig=figure(1)

# create first subplot 
a=fig.add_subplot(111)
for i, cas in enumerate(matrice_cas):
  if cas=='1S_CH4_MP1':
    a.plot(Ti2,Autoignition_cas[i], type_plot[i], color = 'orange', label = cas)
    hold(True)
  else:
    a.plot(Ti2,Autoignition_cas[i], type_plot[i], label = cas)
    hold(True)
title(r'Autoignition delay vs. Temperature')
xlabel(r'Temp [1/K]', fontsize=20)
ylabel("Autoignition [ms]")
a.axis([0.60,0.90,0.0,100.0])
ax = gca()
ax.set_autoscale_on(False)
a.xaxis.set_major_locator(MaxNLocator(7)) # this controls the number of tick marks on the axis
a.yaxis.set_major_locator(MaxNLocator(20))
hold(False)
legend(bbox_to_anchor=(0.9, 0.9,1,1),loc=0)

fig.text(0.5,0.95,r'Autoignition of $CH_{4}$ + Air mixture at $\Phi$ = ' + str(phi) + ', and P = '+str(Pi)+ ' bar',fontsize=22,horizontalalignment='center')
grid()
subplots_adjust(left=0.08, right=0.96, wspace=0.25)

#show()
savefig('Phi'+ str(phi) +'_P'+str(Pi)+'_Trange_'+str(cond)+'.png', bbox_inches='tight')

