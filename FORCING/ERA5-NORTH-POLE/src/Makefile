# Makefile for CDFTOOLS_3.0

# ( make.macro is a link that points to the file macro.xxx where 
#   xxx is representative of your machine )
# !!----------------------------------------------------------------------
# !! CDFTOOLS_3.0 , MEOM 2011
# !! $Id$
# !! Copyright (c) 2010, J.-M. Molines
# !! Software governed by the CeCILL licence (Licence/CDFTOOLSCeCILL.txt)
# !!----------------------------------------------------------------------

include make.macro

BINDIR = bin

VPATH = $(BINDIR)

EXEC = era5_NorthPole

.PHONY: all help clean cleanexe install man installman

all: $(EXEC)

help:
	@echo "#-------------------------------------------------"
	@echo "# List of make targets:"
	@echo "#  all          : build cdftools binary"
	@echo "#  man          : build manual"
	@echo "#  clean        : remove building object (.o, .mod...)"
	@echo "#  cleanexe     : remove binary executable"
	@echo "#  install      : install binary in INSTALL folder"
	@echo "#  install_man  : install manual in INSTALL_MAN folder"
	@echo "#-------------------------------------------------"

## Statistical programs
era5_NorthPole: cdfio.o  era5_NorthPole.f90
	$(F90) era5_NorthPole.f90 -o $(BINDIR)/era5_NorthPole cdfio.o modcdfnames.o $(FFLAGS)

## Modules

cdfio.o: cdfio.F90 modcdfnames.o
	$(F90) -c  cdfio.F90 $(FFLAGS)

modcdfnames.o: modcdfnames.F90 
	$(F90) -c modcdfnames.F90 $(FFLAGS)

## Utilities
clean:
	\rm -f *.mod *.o  *~ *.1 *.opod

cleanexe: clean
	( cd $(BINDIR) ; \rm -f $(EXEC) )

install:
	@mkdir -p $(INSTALL)
	cd ../bin ; \cp $(EXEC)  $(INSTALL)

