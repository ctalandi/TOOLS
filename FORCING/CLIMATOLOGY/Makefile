include make.macro

all: mkclimato.x mkw10.x mkonlyhanning.x mkmodxu.x 

mkclimato.x: mkclimato.f90
	$(F90) $(FFLAGS) mkclimato.f90 -o mkclimato.x $(NCDF)

mkw10.x: mkw10.f90
	$(F90) $(FFLAGS) mkw10.f90 -o mkw10.x $(NCDF)

mkmodxu.x: mkmodxu.f90
	$(F90) $(FFLAGS) mkmodxu.f90 -o mkmodxu.x $(NCDF)

mkonlyhanning.x: mkonlyhanning.f90
	$(F90) $(FFLAGS) mkonlyhanning.f90 -o mkonlyhanning.x $(NCDF)

install: mkclimato.x mkw10.x mkmodxu.x mkonlyhanning.x
	mv  mkclimato.x mkw10.x mkmodxu.x mkonlyhanning.x $(INSTALL)


clean:
	@\rm *~

cleanexe: 
	@\rm mkclimato.x mkw10.x mkmodxu.x mkonlyhanning.x
