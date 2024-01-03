###############################################################################
# Include Snippet for Makefiles
#
#    To create Cantera C++ applications from the install environment
#    include this file into your Makefile environment by putting
#    the line "include Cantera.mak" in your Makefile.
#
#  Main Variables:
#
#      CANTERA_INCLUDES = Variable containing the include path
#      CANTERA_LIBS = List of libraries to include on the link line
#
#      CANTERA_FORTRAN_LIBS = list of libraries to link for Fortran programs
#      CANTERA_FORTRAN_MODS = Directory containing the F90 .mod files
#

CANTERA_VERSION=2.5.0a4

###############################################################################
#        CANTERA CORE
###############################################################################

# The directory where Cantera include files may be found.
#  Include files in application programs should start with:
#     #include "cantera/thermo.h"
#     #include "cantera/kernel/HMWSoln.h"

CANTERA_INSTALL_ROOT=/p/project/dadoren/abdelsamie/dino_libs/cantera/2.4.0

CANTERA_CORE_INCLUDES=-I$(CANTERA_INSTALL_ROOT)/include

CANTERA_EXTRA_INCLUDES= 

# Required Cantera libraries
CANTERA_CORE_LIBS=-pthread -L/p/project/dadoren/abdelsamie/dino_libs/cantera/2.4.0/lib -lcantera

CANTERA_CORE_LIBS_DEP = /p/project/dadoren/abdelsamie/dino_libs/cantera/2.4.0/lib/libcantera.a

CANTERA_EXTRA_LIBDIRS=

CANTERA_CORE_FTN=-L/p/project/dadoren/abdelsamie/dino_libs/cantera/2.4.0/lib -lcantera_fortran -lcantera

CANTERA_FORTRAN_MODS=$(CANTERA_INSTALL_ROOT)/include/cantera

CANTERA_FORTRAN_SYSLIBS=-lpthread -lstdc++

###############################################################################
#            BOOST
###############################################################################

CANTERA_BOOST_INCLUDES=

###############################################################################
#         CVODE/SUNDIALS LINKAGE
###############################################################################

CANTERA_SUNDIALS_INCLUDE=-I/p/project/dadoren/abdelsamie/dino_libs/sundials/3.0.0/include
CANTERA_SUNDIALS_LIBS=-L/p/project/dadoren/abdelsamie/dino_libs/sundials/3.0.0/lib -lsundials_cvodes -lsundials_ida -lsundials_nvecserial

###############################################################################
#         BLAS LAPACK LINKAGE
###############################################################################

CANTERA_BLAS_LAPACK_LIBS=

###############################################################################
#      COMBINATIONS OF INCLUDES AND LIBS
###############################################################################

CANTERA_INCLUDES=$(CANTERA_CORE_INCLUDES) $(CANTERA_SUNDIALS_INCLUDE) \
                 $(CANTERA_BOOST_INCLUDES) $(CANTERA_EXTRA_INCLUDES)

CANTERA_TOTAL_INCLUDES = $(CANTERA_INCLUDES)

# Add this into the compilation environment to identify the version number
CANTERA_DEFINES = -DCANTERA_VERSION=2.5.0a4

CANTERA_LIBS=$(CANTERA_CORE_LIBS) \
             $(CANTERA_EXTRA_LIBDIRS) $(CANTERA_SUNDIALS_LIBS) \
             $(CANTERA_BLAS_LAPACK_LIBS)

CANTERA_TOTAL_LIBS=$(CANTERA_LIBS)

CANTERA_TOTAL_LIBS_DEP= $(CANTERA_CORE_LIBS_DEP) \
                        $(CANTERA_SUNDIALS_LIBS_DEP)

CANTERA_FORTRAN_LIBS=$(CANTERA_CORE_FTN) \
                     $(CANTERA_EXTRA_LIBDIRS) $(CANTERA_SUNDIALS_LIBS) \
                     $(CANTERA_BLAS_LAPACK_LIBS) $(CANTERA_FORTRAN_SYSLIBS)

###############################################################################
#  END
###############################################################################
