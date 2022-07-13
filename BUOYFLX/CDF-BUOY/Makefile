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

EXEC = my_cdfbuoyflx_new

.PHONY: all help clean cleanexe install man installman zclass_list.txt

all: $(EXEC)

help:
	@echo "#-------------------------------------------------"
	@echo "# List of make targets:"
	@echo "#  all          : build cdftools binary"
	@echo "#  man          : build manual"
	@echo "#  clean        : remove building object (.o, .mod...)"
	@echo "#  cleanexe     : remove binary executable"
	@echo "#  install      : install binary in INSTALL folder"
	@echo "#  installman   : install manual in INSTALL_MAN folder"
	@echo "#-------------------------------------------------"

## Statistical programs
my_cdfbuoyflx_new: cdfio.o  eos.o my_cdfbuoyflx_new.f90
	$(F90)  my_cdfbuoyflx_new.f90 -o $(BINDIR)/my_cdfbuoyflx_new cdfio.o eos.o modcdfnames.o $(FFLAGS)

## Modules

cdfio.o: cdfio.F90 modcdfnames.o
	$(F90) -c  cdfio.F90 $(FFLAGS)

eos.o: eos.f90
	$(F90)  -c eos.f90 $(FFLAGS)

modcdfnames.o: modcdfnames.F90 modcdfnames_CMIP6.h90
	$(F90) -c modcdfnames.F90 $(FFLAGS)

modutils.o: cdfio.o modutils.f90
	$(F90) -c modutils.f90 $(FFLAGS)

## Utilities
clean:
	\rm -f *.mod *.o  *~ *.1 *.opod

cleanexe: clean
	( cd $(BINDIR) ; \rm -f $(EXEC) )

man: cdftools.1 cdftools.html

zclass_title.txt:
	grep @class *90 | awk '{print $$NF}' | tr [a-z] [A-Z] | sort -u  | sed -e "s/_/ /g" > zclass_title.txt

zclass_list.txt:
	grep @class *90 | awk '{print $$NF}' |  sort -u  > zclass_list.txt

cdftools.1: cdftools.opod
	pod2man --center "CDFTOOLS / NEMO Documentation" \
	  --release "SVN Revision $$(LANG=C svn update | grep '^At rev' | awk '{print $$3}' | cut -f 1 -d '.')" \
	  cdftools.opod > cdftools.1

cdftools.html: cdftools.opod
	pod2html --infile=cdftools.opod --outfile=cdftools.html --title="CDFTOOLS Man pages" --css="./cdftools.css"

cdftools.opod: $(EXEC) cdftools-begin.pod cdftools-end.pod zclass_list.txt
	cat cdftools-begin.pod > cdftools.opod
	for class in $$( cat zclass_list.txt ) ; do \
           title="$$(echo $$class | tr [a-z] [A-Z] |  sed -e "s/_/ /g")" ; \
	   echo '' >> cdftools.opod ; \
	   echo "=head1 $$title" >> cdftools.opod ; \
	   echo '' >> cdftools.opod ; \
	   for s in $$( grep -e "@class $$class" *90 | awk -F. '{print $$1}' ) ; do echo '' ; echo "=head2 $$s" ; echo ''; $(BINDIR)/$$s; done >> cdftools.opod ; \
	done
	echo '' >> cdftools.opod
	echo "=head1 AUTHORS" >> cdftools.opod
	echo '' >> cdftools.opod
	echo "Project headed  by Jean-Marc Molines, (IGE, Grenoble - France)" >> cdftools.opod
	echo '' >> cdftools.opod
	grep -A1000  -i contribu ../License/CDFTOOLSCeCILL.txt | grep -m1 -B1000 ^$$ >> cdftools.opod
	echo '' >> cdftools.opod
	cat cdftools-end.pod >> cdftools.opod

install:
	@mkdir -p $(INSTALL)
	cd ../bin ; \cp $(EXEC)  $(INSTALL)

installman:
	@mkdir -p $(INSTALL_MAN)/man1;
	\cp -f cdftools.1 $(INSTALL_MAN)/man1/;
	for s in $$( cd $(BINDIR); ls -1 ); do ( cd $(INSTALL_MAN)/man1/; ln -sf cdftools.1 $$s.1 ); done;
	\cp -f cdftools.html ../DOC/
f2py:
	f2py -c --fcompiler=gnu95 -m cdftoolspython cdficediags.f90 cdfio.o modcdfnames.o  -I$(EBROOTNETCDFMINFORTRAN)/include -L$(EBROOTNETCDFMINFORTRAN)/lib64 -lnetcdf -lnetcdff

