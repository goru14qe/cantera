include ./Cantera.mak
#include /p/project/dadoren/abdelsamie/dino_libs/cantera/2.4.0/include/cantera/Cantera.mak

CC=icc
CXX=icpc
RM=rm -f
CXXFLAGS=-vec-report0 -diag-disable 1478 -pthread -O3 -g -std=c++0x
CPPFLAGS=$(CANTERA_INCLUDES)
LDFLAGS=
LDLIBS=$(CANTERA_LIBS)

SRCS=equilbtest.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: equilbtest

clean:
	$(RM) $(OBJS) equilbtest

dist-clean: clean
	$(RM) *~ 
