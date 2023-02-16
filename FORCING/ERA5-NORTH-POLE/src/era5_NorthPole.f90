PROGRAM era5_NorthPole
  !!======================================================================
  !!                     ***  PROGRAM  cdfcurl  ***
  !!=====================================================================
  !!  ** Purpose : Duplicate the line before the last one onto the last line
  !!
  !!  ** Method  : Use the cdfcurl.f90 module as a starting point
  !!
  !! History : 2.1  : 05/2005  : J.M. Molines : Original code
  !!         : 2.1  : 06/2007  : P. Mathiot   : for use with forcing fields
  !!           3.0  : 01/2011  : J.M. Molines : Doctor norm + Lic.
  !!----------------------------------------------------------------------
  USE cdfio
  USE modcdfnames
  !!----------------------------------------------------------------------
  !! CDFTOOLS_3.0 , MEOM 2011
  !! $Id$
  !! Copyright (c) 2011, J.-M. Molines
  !! Software governed by the CeCILL licence (Licence/CDFTOOLSCeCILL.txt)
  !!----------------------------------------------------------------------
  IMPLICIT NONE

  INTEGER(KIND=4)                           :: ji, jj, jt         ! dummy loop index
  INTEGER(KIND=4)                           :: npiglo, npjglo     ! size of the domain
  INTEGER(KIND=4)                           :: npt                ! size of the domain
  INTEGER(KIND=4)                           :: narg, iargc        ! browse command line
  INTEGER(KIND=4)                           :: ijarg              !
  INTEGER(KIND=4)                           :: ncout, incid, ierr  ! browse command line
  INTEGER(KIND=4), DIMENSION(1)             :: ipk, id_varout     ! output variable properties

  REAL(KIND=4), DIMENSION(:),   ALLOCATABLE :: zlat, zlon
  REAL(KIND=8), DIMENSION(:),   ALLOCATABLE :: tim
  REAL(KIND=4), DIMENSION(:,:), ALLOCATABLE :: vtarg

  CHARACTER(LEN=256)                        :: cf_ufil, cf_vfil   ! file names
  CHARACTER(LEN=256)                        :: cf_out = 'era5_npdup.nc' ! output file name
  CHARACTER(LEN=256)                        :: cv_u, cv_v         ! variable names
  CHARACTER(LEN=256)                        :: cldum              ! dummy string

  TYPE (variable), DIMENSION(1)             :: stypvar            ! structure for attibutes

  LOGICAL                                   :: lchk     = .FALSE. ! flag for missing files
  LOGICAL                                   :: ldblpr   = .FALSE. ! flag for dble precision output
  LOGICAL                                   :: lnc4=.false.       ! flag for netcdf4 output with chunking and deflation

  !!----------------------------------------------------------------------
  CALL ReadCdfNames() 

  narg = iargc()
  IF ( narg < 2 ) THEN
     PRINT *,' usage : era5_NorthPole -v file var [-T] [-8]...'
     PRINT *,'           ... [-o OUT-file ]'
     PRINT *,'      '
     PRINT *,'     PURPOSE :'
     PRINT *,'      '
     PRINT *,'     ARGUMENTS :'
     PRINT *,'       -v file var : file and variable name '
     PRINT * 
     PRINT *,'     OPTIONS :'
     PRINT *,'       -8 : save in double precision instead of standard simple precision.'
     PRINT *,'       -nc4 : use netcdf4 output with chunking and deflation 1'
     PRINT *,'       -o OUT-file : specify output file name instead of ',TRIM(cf_out) 
     PRINT *,'      '
     PRINT *,'     OUTPUT : '
     PRINT *,'       netcdf file : ', TRIM(cf_out) 
     STOP
  ENDIF

  ijarg=1
  DO WHILE ( ijarg <= narg ) 
     CALL getarg(ijarg, cldum) ; ijarg=ijarg+1
     SELECT CASE ( cldum )
     CASE ('-v')
        CALL getarg(ijarg, cf_vfil) ; ijarg=ijarg+1
        CALL getarg(ijarg, cv_v   ) ; ijarg=ijarg+1
     CASE ('-8')
        ldblpr = .true.
     CASE ('-o')
        CALL getarg(ijarg, cf_out) ; ijarg=ijarg+1
     CASE DEFAULT
        PRINT *,  TRIM(cldum), ' : unknown option '
     END SELECT
  ENDDO

  lchk = chkfile(cf_vfil ) .OR. lchk
  IF ( lchk ) STOP 99 ! missing files


  ! define new variables for output
  stypvar(1)%cname             = cv_v
  stypvar(1)%cunits            = 'units'
  stypvar(1)%cprecision        ='r4'
  IF ( ldblpr )  stypvar(1)%cprecision     ='r8'
  stypvar(1)%rmissing_value    = -9999.
  stypvar(1)%valid_min         = -1000.
  stypvar(1)%valid_max         =  1000.
  stypvar(1)%clong_name        = 'long name'
  stypvar(1)%cshort_name       = 'var'
  stypvar(1)%conline_operation = 'N/A'
  stypvar(1)%caxis             = 'TYX'

  ipk(1) = 1

  npiglo = getdim(cf_vfil,'longitude')
  npjglo = getdim(cf_vfil,'latitude')
  npt    = getdim(cf_vfil,'time') 

  PRINT *, 'npiglo = ',npiglo
  PRINT *, 'npjglo = ',npjglo
  PRINT *, 'npt    = ',npt

  ! Allocate the memory
  ALLOCATE ( vtarg(npiglo,npjglo) )
  ALLOCATE ( zlat(npjglo) , zlon(npiglo) )


  ! use zun and zvn to store f latitude and longitude for output
  tim  = getvar1d(cf_vfil,      'time',    npt)
  zlat = getvar1d(cf_vfil,  'latitude', npjglo)
  zlon = getvar1d(cf_vfil, 'longitude', npiglo)


  ! create output fileset
  ncout = create      (cf_out, cf_vfil, npiglo, npjglo,  0, cdlonvar='longitude', cdlatvar='latitude', ld_xycoo=.false., ld_nc4=lnc4)
  ierr  = createvar   (ncout , stypvar, 1,      ipk,    id_varout, ld_nc4=lnc4, infileatt=cf_vfil )
  !ierr  = putheadervar(ncout,  cf_vfil, npiglo, npjglo, 1)

  ierr = putvar1d(ncout,    tim,     npt,  'T')
  ierr = putvar1d(ncout,   zlon,  npiglo,  'X')
  ierr = putvar1d(ncout,   zlat,  npjglo,  'Y')

  DO jt=1,npt
     IF (MOD(jt,100)==0 ) PRINT *, jt,'/',npt
        ! read field one record after one 
        vtarg(:,:) =  getvar(cf_vfil, cv_v, 1, npiglo,npjglo, ktime=jt)

        ! duplicate the line before the last one onto the last 
        vtarg(:,1) = vtarg(:,2)
        !
        ierr = putvar(ncout, id_varout(1), vtarg, 1, npiglo, npjglo, ktime=jt)
  END DO

  ierr = closeout(ncout)

  DEALLOCATE ( vtarg, zlat, zlon)

END PROGRAM era5_NorthPole
