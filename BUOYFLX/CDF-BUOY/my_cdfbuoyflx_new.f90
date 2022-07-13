PROGRAM my_cdfbuoyflx_new
  !!======================================================================
  !!                     ***  PROGRAM  my_cdfbuoyflx_new  ***
  !!=====================================================================
  !!  ** Purpose :  Produce a file with the water flux separated into 4 components:
  !!                E (evap), P (precip), R (runoff), dmp (sssdmp).
  !!                The total water flux is E -P -R + dmp. Units in this program
  !!                are mm/days.  (Up to that it is the same than cdfwflx)
  !!
  !!                It also produces un the same file the component of the heat flux
  !!                Latent Heat FLux, Sensible Heat flux, Long Wave HF, Short Wave HF,
  !!                Net HF
  !!
  !!                Buoyancy fluxes are also computed, as a net value but also with the
  !!                contribution of each term.
  !!
  !!  ** Method  : Evap is computed from the latent heat flux : evap=-qla/Lv
  !!               Runoff is read from the climatological input file
  !!               dmp is read from the file (sowafldp)
  !!               Precip is then computed as the difference between the
  !!               total water flux (sowaflup) and the E-R+dmp. In the high latitudes
  !!               this precip includes the effect of snow (storage/melting). Therefore
  !!               it may differ slightly from the input precip file.
  !!
  !!               Heat fluxes are directly copied from the gridT files, same name, same units
  !!               We also add sst and SSS for convenience.
  !!
  !!               Buoyancy fluxes are also computed as :
  !!                  BF = g/rho ( alpha x TF  - beta x SF ) 
  !!                       (TF = thermal part, SF = haline part )
  !!                  TF = Qnet/cp
  !!                  SF = rho x (E-P) x SSS
  !!  ** Reference :
  !!              Atmosphere, Ocean and Climate Dynamics: An Introductory Text. By John Marshall,
  !!              R. Alan Plumb ( Academic Press, 2008 ) Eq. 11.4 p 225. 
  !!
  !! History : 2.1  : 01/2008  : J.M. Molines : Original code
  !!           3.0  : 12/2010  : J.M. Molines : Doctor norm + Lic.
  !!           3.0  : 09/2015  : J.M. Molines : add nc4 capabilities, optional output file
  !!                                            short output,
  !!                                            different management of read fluxes (XIOS ...)
  !!----------------------------------------------------------------------
  USE cdfio
  USE eos
  USE modcdfnames
  !!----------------------------------------------------------------------
  !! CDFTOOLS_3.0 , MEOM 2011
  !! $Id$
  !! Copyright (c) 2010, J.-M. Molines
  !! Software governed by the CeCILL licence (Licence/CDFTOOLSCeCILL.txt)
  !!----------------------------------------------------------------------
  IMPLICIT NONE

  INTEGER(KIND=4)                           :: np_varout=25
  INTEGER(KIND=4)                           :: ncout, ierr
  INTEGER(KIND=4)                           :: jt                                ! dummy loop index
  INTEGER(KIND=4)                           :: narg, iargc, ijarg                ! command line 
  INTEGER(KIND=4)                           :: npiglo, npjglo, npt               ! size of the domain
  INTEGER(KIND=4), ALLOCATABLE, DIMENSION(:):: ipk, id_varout  

  ! Physical constants
  REAL(KIND=4)                              :: Lv = 2.5e6                        ! latent HF <--> evap conversion
  REAL(KIND=4)                              :: Cp = 4000.                        ! specific heat of water 
  REAL(KIND=4)                              :: Rho = 1026.                       ! reference density
  REAL(KIND=4)                              :: Grav = 9.81                       ! Gravity

  REAL(KIND=4), DIMENSION(:),   ALLOCATABLE :: tim, zdep                         ! time counter, deptht
  REAL(KIND=4), DIMENSION(:,:), ALLOCATABLE :: zmask, zcoefq, zcoefw             ! work array
  REAL(KIND=4), DIMENSION(:,:), ALLOCATABLE :: zalbet, zbeta                     ! work array
  REAL(KIND=4), DIMENSION(:,:), ALLOCATABLE :: EmP, wice, runoff, wdmp, wnet     ! water flux components
  REAL(KIND=4), DIMENSION(:,:), ALLOCATABLE :: qsol, qnsol, qnet                 ! heat flux components
  REAL(KIND=4), DIMENSION(:,:), ALLOCATABLE :: b_EmP, b_wice, b_runoff, b_wdmp, bw_net        ! BF water flux components
  REAL(KIND=4), DIMENSION(:,:), ALLOCATABLE :: b_qsol, b_qnsol, bh_net                        ! BF heat flux components
  REAL(KIND=4), DIMENSION(:,:), ALLOCATABLE :: zsst, zsss, buoyancy_fl           ! Total buoyancy flux

  CHARACTER(LEN=256)                        :: cf_tfil ,cf_flxfil, cf_rnfil      ! input file gridT, flx and runoff
  CHARACTER(LEN=256)                        :: cf_out='buoyflx.nc'               ! output file
  CHARACTER(LEN=256)                        :: cldum                             ! dummy character variable
  CHARACTER(LEN=256)                        :: cv_sss                            ! Actual name for SSS
  CHARACTER(LEN=256)                        :: cv_sst                            ! Actual name for SST

  TYPE(variable), ALLOCATABLE, DIMENSION(:) :: stypvar                           ! structure for attributes

  LOGICAL                                   :: lchk =.false.                     ! flag for missing files
  LOGICAL                                   :: lnc4 =.false.                     ! flag for netcdf4 output
  LOGICAL                                   :: lsho =.false.                     ! flag for short output
  !!----------------------------------------------------------------------
  CALL ReadCdfNames()

  !!  Read command line and output usage message if not compliant.
  narg= iargc()
  IF ( narg == 0 ) THEN
     PRINT *,' usage : cdfbuoyflx  -t T-file [-r RNF-file] [-f FLX-file ] [-sss SSS-name]'
     PRINT *,'     ... [-sst SST-name] [-nc4] [-o output_file]  [-short ]'
     PRINT *,'      '
     PRINT *,'     PURPOSE :'
     PRINT *,'       Compute (or read) the heat and water fluxes components.'
     PRINT *,'       Compute (or read) the net heat and water fluxes.'
     PRINT *,'       Compute the buoyancy heat and water fluxes components.'
     PRINT *,'       Compute the net buoyancy fluxes.'
     PRINT *,'       Save sss and sst. '
     PRINT *,'      '
     PRINT *,'     ARGUMENTS :'
     PRINT *,'       -t T-file   : netcdf file with temperature and salinity '
     PRINT *,'      '
     PRINT *,'      '
     PRINT *,'     OPTIONS :'
     PRINT *,'       [ -r RNF-file ] : Specify a run-off file if runoff not in T-file '
     PRINT *,'                         nor in FLX-file'
     PRINT *,'       [ -f FLX-file ] : Use this option if fluxes are not saved in gridT files'
     PRINT *,'       [ -sss SSS-name ] : Use this option if SSS variable name in T-file '
     PRINT *,'                          differ from ',TRIM(cn_vosaline)
     PRINT *,'       [ -sst SST-name ] : Use this option if SST variable name in T-file '
     PRINT *,'                          differ from ',TRIM(cn_votemper)
     PRINT *,'       [ -nc4 ] Use netcdf4 output with chunking and deflation level 1'
     PRINT *,'               This option is effective only if cdftools are compiled with'
     PRINT *,'               a netcdf library supporting chunking and deflation.'
     PRINT *,'       [ -o output_file ] Default is ', TRIM(cf_out)
     PRINT *,'       [ -short ] With this option only save the buoyancy flux without '
     PRINT *,'                  all the components of the flux.'
     PRINT *,'      '
     PRINT *,'     REQUIRED FILES :'
     PRINT *,'        none'
     PRINT *,'      '
     PRINT *,'     OUTPUT : '
     PRINT *,'       netcdf file : ', TRIM(cf_out) 
     PRINT *,'         variables : 25 variables (2D) or 1 variable in case of -short option'
     PRINT *,'      '
     PRINT *,'     SEE ALSO :'
     PRINT *,'      '
     PRINT *,'      '
     STOP
  ENDIF
  ijarg   = 1
  cf_flxfil='none'
  cf_rnfil='none'
  cv_sss=cn_vosaline
  cv_sst=cn_votemper 
 
  DO   WHILE ( ijarg <= narg ) 
     CALL getarg (ijarg, cldum) ; ijarg = ijarg + 1
     SELECT CASE ( cldum )
     CASE ( '-f' )     ! specify  flx files
        CALL getarg (ijarg, cf_flxfil) ; ijarg = ijarg + 1
        lchk = lchk .OR. chkfile (cf_flxfil)
     CASE ( '-t' )     ! specify  T files
        CALL getarg (ijarg, cf_tfil) ; ijarg = ijarg + 1
        lchk = lchk .OR. chkfile (cf_tfil  )
     CASE ( '-r' )     ! specify  runoff files
        CALL getarg (ijarg, cf_rnfil) ; ijarg = ijarg + 1
        lchk = lchk .OR. chkfile (cf_rnfil )
     CASE ( '-sss' )     ! specify  runoff files
        CALL getarg (ijarg, cv_sss) ; ijarg = ijarg + 1
     CASE ( '-sst' )     ! specify  runoff files
        CALL getarg (ijarg, cv_sst) ; ijarg = ijarg + 1
     CASE ( '-nc4' )   !  allow chunking and deflation on output
        lnc4 = .true.
     CASE ( '-o' )     ! specify  output files
        CALL getarg (ijarg, cf_out) ; ijarg = ijarg + 1
     CASE ( '-short' ) ! use short output ( only buoyancy fluxes )
        lsho = .true. ; np_varout = 3
     CASE DEFAULT
        PRINT *, " Option ", TRIM(cldum)," not supported "
        STOP
     END SELECT
  ENDDO
  IF (lchk ) STOP ! missing files

  IF ( cf_flxfil == 'none' ) THEN
    cf_flxfil = cf_tfil
  ENDIF
  ! If no runoff file specified, assume that run off are in flx file [ which must be read by the way ... ]
  IF ( cf_rnfil == 'none' ) THEN
    cf_rnfil = cf_flxfil
  ENDIF

  npiglo = getdim (cf_tfil,cn_x)
  npjglo = getdim (cf_tfil,cn_y)
  npt    = getdim (cf_tfil,cn_t)

  PRINT *, 'npiglo =', npiglo
  PRINT *, 'npjglo =', npjglo
  PRINT *, 'npt    =', npt

  CALL CreateOutput

  ! always allocated
  ALLOCATE ( zmask(npiglo,npjglo), wnet(npiglo,npjglo), zalbet(npiglo,npjglo), zbeta(npiglo, npjglo) )
  ALLOCATE ( zcoefq(npiglo,npjglo), zcoefw(npiglo,npjglo), qnet(npiglo,npjglo) )
  ALLOCATE ( bw_net(npiglo,npjglo) ,bh_net(npiglo,npjglo)) 
  ALLOCATE ( buoyancy_fl(npiglo,npjglo), zsst(npiglo,npjglo), zsss(npiglo,npjglo) )

  ! allocated only for full output
  IF ( .NOT. lsho ) THEN
  ALLOCATE ( EmP(npiglo,npjglo), runoff(npiglo,npjglo), wdmp(npiglo,npjglo), wice(npiglo,npjglo))
  ALLOCATE ( qsol(npiglo,npjglo), qnsol(npiglo,npjglo))
  ALLOCATE ( b_EmP(npiglo,npjglo), b_runoff(npiglo,npjglo), b_wdmp(npiglo,npjglo), b_wice(npiglo,npjglo)) 
  ALLOCATE ( b_qsol(npiglo,npjglo), b_qnsol(npiglo,npjglo))
  ENDIF

  DO jt = 1, npt
     ! read sss for masking purpose and sst
     zsss(:,:) = getvar(cf_tfil, cv_sss, 1, npiglo, npjglo, ktime=jt)
     zmask=1. ; WHERE ( zsss == 0 ) zmask=0.
     zsst(:,:) = getvar(cf_tfil, cv_sst, 1, npiglo, npjglo, ktime=jt)

     ! total water flux 
     wnet(:,:) = getvar(cf_flxfil, 'empmr', 1, npiglo, npjglo, ktime=jt )*86400.*zmask(:,:)          ! mm/days  positive out
      ! total heat flux 
     qnet(:,:)=  getvar(cf_flxfil, 'qt', 1, npiglo, npjglo, ktime=jt )*zmask(:,:)    ! W/m2  positive in

     ! buoyancy flux
     zalbet(:,:)= albet ( zsst, zsss, 0., npiglo, npjglo)
     zbeta (:,:)= beta  ( zsst, zsss, 0., npiglo, npjglo)
     zcoefq(:,:)= Grav/Rho *( zbeta * zalbet /Cp ) * 1.e6
     zcoefw(:,:)= Grav* zbeta * zsss / 86400. /1000 * 1.e6   ! division by 86400 and 1000 to get back water fluxes in m/s

     buoyancy_fl=0. ; bh_net=0. ; bw_net=0.
     WHERE ( zmask == 1 ) 
        bh_net(:,:)= zcoefq * qnet
        bw_net(:,:)= zcoefw * wnet
        buoyancy_fl(:,:) = ( bh_net - bw_net ) 
     END WHERE

     IF ( .NOT. lsho ) THEN
     ! EP : 
     EmP(:,:)= getvar(cf_flxfil, 'emp_oce', 1, npiglo, npjglo, ktime=jt)*86400.*zmask(:,:)    ! mm/days positive out

     ! Damping
     wdmp(:,:)= getvar(cf_flxfil, 'wfcorr', 1, npiglo, npjglo, ktime=jt)*86400.*zmask(:,:) ! mm/days positive out

     ! Runoff  
     runoff(:,:)= getvar(cf_flxfil, 'runoffs', 1, npiglo, npjglo, ktime=jt)*-1.*86400.*zmask(:,:)         ! mm/days change sign to get positive out

     ! fsalt = contribution of ice freezing and melting to salinity ( + = freezing, - = melting )
     wice(:,:) = getvar(cf_flxfil, 'fmmflx', 1, npiglo, npjglo, ktime=jt )*86400.*zmask(:,:)          ! mm/days positive out
 
     ! heat fluxes
     qsol(:,:)= getvar(cf_flxfil, 'rsntds',  1, npiglo, npjglo, ktime = jt )*zmask(:,:)    ! W/m2 positive in
     qnsol(:,:)= getvar(cf_flxfil, 'nshfls',  1, npiglo, npjglo, ktime = jt )*zmask(:,:)    ! W/m2 positive in


     b_qsol=0.  ; b_qnsol=0.   
     b_EmP=0.   ; b_wdmp=0.  ; b_wice=0.     ; b_runoff=0.


     WHERE (zsss /= 0 ) 
        b_qsol(:,:)= zcoefq * qsol
        b_qnsol (:,:)= zcoefq * qnsol

        b_EmP(:,:)= zcoefw * EmP
        b_wice(:,:)= zcoefw * wice
        b_runoff(:,:)= zcoefw * runoff
        b_wdmp(:,:)= zcoefw * wdmp

        !    buoyancy_fl(:,:) = zcoefq * qnet +zcoefw * wnet
     END WHERE
     ENDIF

     ! Write output file
     IF ( lsho ) THEN
        ierr = putvar(ncout, id_varout(1),buoyancy_fl, 1,npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(2),bw_net     , 1,npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(3),bh_net     , 1,npiglo, npjglo, ktime=jt )

     ELSE
        ierr = putvar(ncout, id_varout(1), EmP,    1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(2), wice,   1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(3), runoff, 1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(4), wdmp,   1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(5), wnet,   1, npiglo, npjglo, ktime=jt )

        ierr = putvar(ncout, id_varout(6), qsol,     1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(7), qnsol,    1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(8), qnet,     1, npiglo, npjglo, ktime=jt )

        ierr = putvar(ncout, id_varout(9),  b_EmP,    1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(10), b_wice,   1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(11), b_runoff, 1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(12), b_wdmp,   1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(13), bw_net,  1, npiglo, npjglo, ktime=jt )

        ierr = putvar(ncout, id_varout(14), b_qsol,     1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(15), b_qnsol,    1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(16), bh_net,    1, npiglo, npjglo, ktime=jt )

        ierr = putvar(ncout, id_varout(17),buoyancy_fl, 1,npiglo, npjglo, ktime=jt )

        ierr = putvar(ncout, id_varout(18), zsss,  1, npiglo, npjglo, ktime=jt )
        ierr = putvar(ncout, id_varout(19), zsst,  1, npiglo, npjglo, ktime=jt )
     ENDIF
  END DO  ! time loop

  tim  = getvar1d(cf_tfil, cn_vtimec, npt     )
  ierr = putvar1d(ncout,   tim,       npt, 'T')

  ierr=closeout(ncout)

CONTAINS
  SUBROUTINE CreateOutput
    !!---------------------------------------------------------------------
    !!                  ***  ROUTINE CreateOutput  ***
    !!
    !! ** Purpose :  Set up all things required for the output file, create
    !!               the file and write the header part.
    !!
    !! ** Method  :  Use global module variables
    !!
    !!----------------------------------------------------------------------
    INTEGER(KIND=4) :: jv   ! dummy loop index
    !!----------------------------------------------------------------------
    ! prepare output variables
    ALLOCATE (zdep(1), tim(npt) )
    zdep(1) = 0.
    ALLOCATE (ipk(np_varout), id_varout(np_varout), stypvar(np_varout) )
    ipk(:)  = 1  ! all variables ( output are 2D)
    stypvar%conline_operation = 'N/A'
    stypvar%caxis             = 'TYX'
    DO jv = 1, np_varout
       stypvar(jv)%ichunk = (/npiglo,MAX(1,npjglo/30), 1, 1 /)
    ENDDO

    IF ( lsho ) THEN
       ! total buoyancy flux
       stypvar(1)%cname= 'buoyancy_fl'
       stypvar(1)%cunits='1e-6 m2/s3'
       stypvar(1)%rmissing_value=0.
       stypvar(1)%valid_min= -100.
       stypvar(1)%valid_max= 100.
       stypvar(1)%clong_name='buoyancy flux'
       stypvar(1)%cshort_name='buoyancy_fl'

       ! Water buoyancy flux
       stypvar(2)%cname= 'watnet_b'
       stypvar(2)%cunits='1e-6 m2/s3'
       stypvar(2)%rmissing_value=1.e+20
       stypvar(2)%valid_min= -100.
       stypvar(2)%valid_max= 100.
       stypvar(2)%clong_name='buoy haline flx '
       stypvar(2)%cshort_name='watnet_b'

       ! Heat buoyancy flux
       stypvar(3)%cname= 'heatnet_b'
       stypvar(3)%cunits='1e-6 m2/s3'
       stypvar(3)%rmissing_value=1.e+20
       stypvar(3)%valid_min= -100.
       stypvar(3)%valid_max= 100.
       stypvar(3)%clong_name='buoy thermo Flux'
       stypvar(3)%cshort_name='heatnet_b'

    ELSE
       ! 1--> 5 water fluxes                     ;   ! 6 --> 8    heat fluxes
       stypvar(1)%cname= 'EmP'                   ;  stypvar(6)%cname= 'solar'      
       stypvar(2)%cname= 'wice'                  ;  stypvar(7)%cname= 'nonsolar'      
       stypvar(3)%cname= 'runoff'                ;  stypvar(8)%cname= 'heatnet'      
       stypvar(4)%cname= 'sssdmp'                       
       stypvar(5)%cname= 'watnet'                       

       stypvar(1:5)%cunits='mm/day'                            ;  stypvar(6:8)%cunits='W/m2'      
       stypvar(1:5)%rmissing_value=0.                          ;  stypvar(6:8)%rmissing_value=0.      
       stypvar(1:5)%valid_min= -100.                           ;  stypvar(6:8)%valid_min= -500.      
       stypvar(1:5)%valid_max= 100.                            ;  stypvar(6:8)%valid_max= 500.      
       stypvar(1)%clong_name='Evap. - Precip.'                 ;  stypvar(6)%clong_name='Solar Heat flux'      
       stypvar(2)%clong_name='Ice congelation and melting'     ;  stypvar(7)%clong_name='Non Solar Heat flux'       
       stypvar(3)%clong_name='Runoff'                          ;  stypvar(8)%clong_name='Net Heat Flux'      
       stypvar(4)%clong_name='SSS damping'       
       stypvar(5)%clong_name='Total water flux'        

       stypvar(1)%cshort_name='EmP'              ;  stypvar(6)%cshort_name='solar'      
       stypvar(2)%cshort_name='wice'             ;  stypvar(7)%cshort_name='nonsolar'      
       stypvar(3)%cshort_name='runoff'           ;  stypvar(8)%cshort_name='heatnet'      
       stypvar(4)%cshort_name='sssdmp'           
       stypvar(5)%cshort_name='watnet'                

       ! 9--> 13  buoy water fluxes             ;   ! 14 --> 16    buoy heat fluxes
       stypvar(9)%cname= 'EmP_b'                 ;  stypvar(14)%cname= 'solar_b'
       stypvar(10)%cname= 'wice_b'               ;  stypvar(15)%cname= 'nonsolar_b'
       stypvar(11)%cname= 'runoff_b'             ;  stypvar(16)%cname= 'heatnet_b'
       stypvar(12)%cname= 'sssdmp_b'             
       stypvar(13)%cname= 'watnet_b'            
      
       stypvar(9:13)%cunits='1e-6 m2/s3'        ;  stypvar(14:16)%cunits='1e-6 m2/s3'
       stypvar(9:13)%rmissing_value=0.          ;  stypvar(14:16)%rmissing_value=0.
       stypvar(9:13)%valid_min= -100.           ;  stypvar(14:16)%valid_min= -500.
       stypvar(9:13)%valid_max= 100.            ;  stypvar(14:16)%valid_max= 500.

       stypvar(9)%clong_name='buoy flx E-P'     ;  stypvar(14)%clong_name='buoy Solar Heat flux'
       stypvar(10)%clong_name='buoy flx ice'    ;  stypvar(15)%clong_name='buoy Non Solar Heat flux'
       stypvar(11)%clong_name='buoy flx runoff' ;  stypvar(16)%clong_name='buoy thermo Flux'
       stypvar(12)%clong_name='buoy flx damping' 
       stypvar(13)%clong_name='buoy haline flx'  

       stypvar(9)%cshort_name='EmP_b'            ;  stypvar(14)%cshort_name='solar_b'
       stypvar(10)%cshort_name='wice_b'          ;  stypvar(15)%cshort_name='nonsolar_b'
       stypvar(11)%cshort_name='runoff_b'        ;  stypvar(16)%cshort_name='heatnet_b'
       stypvar(12)%cshort_name='sssdmp_b'       
       stypvar(13)%cshort_name='watnet_b'        

       ! total buoyancy flux
       stypvar(17)%cname= 'buoyancy_fl'
       stypvar(17)%cunits='1e-6 m2/s3'
       stypvar(17)%rmissing_value=0.
       stypvar(17)%valid_min= -100.
       stypvar(17)%valid_max= 100.
       stypvar(17)%clong_name='buoyancy flux'
       stypvar(17)%cshort_name='buoyancy_fl'

       ! SSS                                         ; SST
       stypvar(18)%cname= 'sss'                      ;   stypvar(19)%cname= 'sst'
       stypvar(18)%cunits='PSU'                      ;   stypvar(19)%cunits='Celsius'
       stypvar(18)%rmissing_value=0.                 ;   stypvar(19)%rmissing_value=0.
       stypvar(18)%valid_min= 0.                     ;   stypvar(19)%valid_min= -2.
       stypvar(18)%valid_max= 45                     ;   stypvar(19)%valid_max= 45
       stypvar(18)%clong_name='Sea Surface Salinity' ;   stypvar(19)%clong_name='Sea Surface Temperature'
       stypvar(18)%cshort_name='sss  '               ;   stypvar(19)%cshort_name='sst'
    ENDIF

    ncout = create      (cf_out, cf_tfil, npiglo,    npjglo, 1,          ld_nc4=lnc4 )
    ierr  = createvar   (ncout,  stypvar, np_varout, ipk,    id_varout , ld_nc4=lnc4 )
    ierr  = putheadervar(ncout,  cf_tfil, npiglo,    npjglo, 1,   pdep=zdep )
  END SUBROUTINE CreateOutput


END PROGRAM my_cdfbuoyflx_new
