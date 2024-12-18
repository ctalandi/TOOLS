PROGRAM cdfeke
  !!======================================================================
  !!                     ***  PROGRAM cdfeke   ***
  !!=====================================================================
  !!  ** Purpose : Compute Eddy Kinetic Energy 
  !!
  !!  ** Method  : Use gridU gridV files 
  !!               Velocities are interpolated both on T points
  !!               and the variance is computed. If -mke option is used
  !!               the program also outputs MKE field
  !!
  !! History : pre  : 11/2004  : J.M. Molines : Original code
  !!           2.1  : 04/2005  : J.M. Molines : use modules
  !!           3.0  : 12/2010  : J.M. Molines : Doctor norm + Lic.
  !!         : 4.0  : 03/2017  : J.M. Molines  
  !!----------------------------------------------------------------------
  USE cdfio 
  USE modcdfnames
  !!----------------------------------------------------------------------
  !! CDFTOOLS_4.0 , MEOM 2017 
  !! $Id$
  !! Copyright (c) 2017, J.-M. Molines 
  !! Software governed by the CeCILL licence (Licence/CDFTOOLSCeCILL.txt)
  !! @class derived_fields
  !!----------------------------------------------------------------------
  IMPLICIT NONE

  INTEGER(KIND=4)                            :: ji, jj, jk, jt      ! dummy loop index
  INTEGER(KIND=4)                            :: narg, iargc         ! command line browsing
  INTEGER(KIND=4)                            :: ijarg               ! command line browsing
  INTEGER(KIND=4)                            :: npiglo, npjglo      ! size of the domain (horiz)
  INTEGER(KIND=4)                            :: npk, npt            ! size of the domain vert and time
  INTEGER(KIND=4)                            :: ncout               ! ncid of output file
  INTEGER(KIND=4)                            :: ierr                ! Error status
  INTEGER(KIND=4)                            :: ivar                ! variable counter
  INTEGER(KIND=4)                            :: ip_eke, ip_mke, ip_tke  ! variable index
  INTEGER(KIND=4), DIMENSION(3)              :: ipk, id_varout      ! 

  REAL(KIND=4)                               :: ua, va, upT, vpT    ! working arrays
  REAL(KIND=4), DIMENSION (:,:), ALLOCATABLE :: uc, vc, um, vm      ! velocities etc...
  REAL(KIND=4), DIMENSION (:,:), ALLOCATABLE :: eke                 ! velocities etc...
  REAL(KIND=4), DIMENSION (:,:), ALLOCATABLE :: tke                 ! Mean Kinetic energy
  REAL(KIND=4), DIMENSION (:,:), ALLOCATABLE :: rmke                ! Kinetic energy of the mean flow
  REAL(KIND=8), DIMENSION(:),    ALLOCATABLE :: dtim                ! time variable

  CHARACTER(LEN=256)                         :: cf_out='eke.nc'     ! file name
  CHARACTER(LEN=256)                         :: cf_ufil, cf_umfil   ! file name
  CHARACTER(LEN=256)                         :: cf_vfil, cf_vmfil   !   "
  CHARACTER(LEN=256)                         :: cf_tfil             !   "
  CHARACTER(LEN=256)                         :: cldum               ! dummy character variable
  CHARACTER(LEN=256)                         :: cl_vozocrtx         ! local name of U component
  CHARACTER(LEN=256)                         :: cl_vozocrtxm        ! local name of U mean component
  CHARACTER(LEN=256)                         :: cl_vomecrty         ! local name of V component
  CHARACTER(LEN=256)                         :: cl_vomecrtym        ! local name of V2 component

  TYPE(variable), DIMENSION(3)               :: stypvar             !

  LOGICAL                                    :: lchk                ! checking files existence
  LOGICAL                                    :: lperio = .FALSE.    ! checking E-W periodicity
  LOGICAL                                    :: leke   = .TRUE.     ! compute EKE
  LOGICAL                                    :: lmke   = .FALSE.    ! compute MKE
  LOGICAL                                    :: ltke   = .FALSE.    ! compute TKE
  LOGICAL                                    :: lnc4   = .FALSE.    ! netcdf4 output (chunking and deflation)
  LOGICAL                                    :: lsurf  = .FALSE.    ! flag to set for file w/o vertical dims
  !!----------------------------------------------------------------------
  CALL ReadCdfNames()

  !!  Read command line
  narg= iargc()
  IF ( narg == 0 ) THEN
     PRINT *,' usage : cdfene -u U-file -um U-file -v V-file -vm V-file -t T-file ...'
     PRINT *,'               [-surf] [-mke] [-tke] ...'
     PRINT *,'               [-o OUT-file] [-nc4][-var VAR-u VAR-v] '
     PRINT *,'      '
     PRINT *,'     PURPOSE :'
     PRINT *,'        Compute the Eddy Kinetic Energy from previously computed mean values'
     PRINT *,'      '
     PRINT *,'     ARGUMENTS : both ''General Use'' or ''Reduced Use'' are acceptable'
     PRINT *,'      * General Use: 5 files are given in argument, and EKE is computed'
     PRINT *,'       -u  U-file  : gridU type file with U component.' 
     PRINT *,'       -um U-file  : gridU type file with mean U component.' 
     PRINT *,'       -v  V-file  : gridV type file with V component.' 
     PRINT *,'       -vm V-file  : gridV type file with mean V component.' 
     PRINT *,'       -t  T-file  : any gridT or gridT2 (smaller) file, used for EKE header.'
     PRINT *,'       '
     PRINT *,'      * Reduced Use: no U2/V2 file, only MKE is computed from U and V file.'
     PRINT *,'       -u U-file  : gridU type file with mean U component.' 
     PRINT *,'       -v V-file  : gridV type file with mean V component.' 
     PRINT *,'       -t T-file  : any gridT or gridT2 (smaller) file, used for MKE header.'
     PRINT *,'             '
     PRINT *,'     OPTION :'
     PRINT *,'       [-surf] : Use this option if the T-file has no vertical dimension.'
     PRINT *,'       [-mke]  : output MKE (KE of mean flow) field together with EKE. '
     PRINT *,'       [-tke]  : output TKE (Mean KE of flow) field together with EKE. '
     PRINT *,'       [-nc4]  : allow netcdf4 output with compression and chunking.'
     PRINT *,'       [-o output file]: specify output file name instead of ', TRIM(cf_out)
     PRINT *,'       [-var VAR-u VAR-v VAR-um VAR-vm]: specify the name of the mean and '
     PRINT *,'            mean-squared velocity components if they differ from the standard'
     PRINT *,'            names :',TRIM(cn_vozocrtx),', ',TRIM(cn_vozocrtx)//'_sqd, ' &
       &                          ,TRIM(cn_vomecrty),', ',TRIM(cn_vomecrty)//'_sqd'
     PRINT *,'      '
     PRINT *,'     REQUIRED FILES :'
     PRINT *,'        none'
     PRINT *,'      '
     PRINT *,'     OUTPUT : '
     PRINT *,'       netcdf file : ', TRIM(cf_out) , ' unless -o option in use.'
     PRINT *,'         variables : voeke (m2/s)'
     PRINT *,'         variables : vomke (m2/s) if required'
     PRINT *,'         variables : votke (m2/s) if required'
     PRINT *,'      '
     STOP
  ENDIF
  !!
  !! Initialisation from 1st file (all file are assume to have the same geometry)
  cf_umfil='none' ; cf_vmfil='none'
  cl_vozocrtx  = cn_vozocrtx
  cl_vozocrtxm = cn_vozocrtx
  cl_vomecrty  = cn_vomecrty
  cl_vomecrtym = cn_vomecrty
  ip_eke=0        ; ip_mke=0
  ijarg = 1 
  DO WHILE ( ijarg <= narg )
     CALL getarg(ijarg, cldum ) ; ijarg = ijarg + 1
     SELECT CASE ( cldum )
     CASE ( '-u'   ) ; CALL getarg(ijarg, cf_ufil  ) ; ijarg = ijarg + 1
     CASE ( '-um'  ) ; CALL getarg(ijarg, cf_umfil ) ; ijarg = ijarg + 1
     CASE ( '-v'   ) ; CALL getarg(ijarg, cf_vfil  ) ; ijarg = ijarg + 1
     CASE ( '-vm'  ) ; CALL getarg(ijarg, cf_vmfil ) ; ijarg = ijarg + 1
     CASE ( '-t'   ) ; CALL getarg(ijarg, cf_tfil  ) ; ijarg = ijarg + 1
     CASE ( '-mke' ) ; lmke = .TRUE.
     CASE ( '-surf') ; lsurf= .TRUE.
     CASE ( '-tke' ) ; ltke = .TRUE.
     CASE ( '-nc4' ) ; lnc4 = .TRUE.
     CASE ( '-o'   ) ; CALL getarg(ijarg, cf_out   ) ; ijarg = ijarg + 1
     CASE ( '-var' ) ; CALL getarg(ijarg, cl_vozocrtx  ) ; ijarg = ijarg + 1
       ;             ; CALL getarg(ijarg, cl_vomecrty  ) ; ijarg = ijarg + 1
       ;             ; CALL getarg(ijarg, cl_vozocrtxm ) ; ijarg = ijarg + 1
       ;             ; CALL getarg(ijarg, cl_vomecrtym ) ; ijarg = ijarg + 1
     CASE DEFAULT    ; PRINT *,' ERROR : ',TRIM(cldum),' : unknown option.'
     END SELECT
  ENDDO

  ! if after parsing the command line cf_umfil or cf_vmfil are still 'none'
  ! then only mke will be computed. (Reduced Use)
  IF ( cf_umfil == 'none' .OR.  cf_vmfil == 'none' ) THEN 
     lmke = .TRUE.
     leke = .FALSE.
     ltke = .FALSE.
  ENDIF

  lchk =           chkfile (cf_ufil )
  lchk = lchk .OR. chkfile (cf_vfil )
  lchk = lchk .OR. chkfile (cf_tfil )
  IF (  leke ) THEN
     lchk = lchk .OR. chkfile (cf_umfil)
     lchk = lchk .OR. chkfile (cf_vmfil)
  ENDIF

  IF ( lchk ) STOP 99 ! missing files

  npiglo = getdim (cf_ufil,cn_x)
  npjglo = getdim (cf_ufil,cn_y)
  npk    = getdim (cf_ufil,cn_z)
  npt    = getdim (cf_ufil,cn_t)

  IF ( npk == 0 ) npk=1 ! assume 1 level at least

  PRINT *, 'npiglo = ', npiglo
  PRINT *, 'npjglo = ', npjglo
  PRINT *, 'npk    = ', npk
  PRINT *, 'npt    = ', npt

  ALLOCATE( uc(npiglo,npjglo), vc(npiglo,npjglo) )
  IF ( leke ) THEN
     ALLOCATE( eke(npiglo,npjglo)  )
     ALLOCATE( um(npiglo,npjglo), vm(npiglo,npjglo) )
     eke(:,:) = 0.e0
  ENDIF

  IF (lmke ) THEN
     ALLOCATE( rmke(npiglo,npjglo)  )
     rmke(:,:) = 0.e0
  ENDIF
  IF (ltke ) THEN
     ALLOCATE( tke(npiglo,npjglo)  )
     tke(:,:) = 0.e0
  ENDIF


  ALLOCATE( dtim(npt) )

  CALL CreateOutput
  ! check for E_W periodicity
  uc(:,:) = getvar(cf_tfil, cn_vlon2d, 1, npiglo, npjglo )
  IF ( uc(1,1) ==  uc(npiglo-1,1) ) THEN 
     lperio = .TRUE. 
     PRINT *,' E-W periodicity detected '
  ENDIF

  DO jt = 1, npt  ! input file is likely to contain only one time frame but who knows ...
     DO jk = 1, npk
        ! Read the full velocity field 
        uc(:,:) = getvar(cf_ufil,  cl_vozocrtx,               jk, npiglo, npjglo, ktime=jt )
        vc(:,:) = getvar(cf_vfil,  cl_vomecrty,               jk, npiglo, npjglo, ktime=jt )
        IF ( leke ) THEN
           ! Read the mean velocity field 
           um(:,:) = getvar(cf_umfil, cl_vozocrtxm, jk ,npiglo, npjglo, ktime=jt )
           vm(:,:) = getvar(cf_vmfil, cl_vomecrtym, jk ,npiglo, npjglo, ktime=jt )
        ENDIF

        ua=0.  ;  va=0.  ;  upT = 0. ; vpT = 0. ; eke(:,:) = 0.

        IF ( leke ) THEN
           DO ji=2, npiglo
              DO jj=2,npjglo
                 ! Compute the u/v prime square at T-point
                 upT = 0.5* ( ( uc(ji,jj)-um(ji,jj) )*( uc(ji,jj)-um(ji,jj) ) + ( uc(ji-1,jj)-um(ji-1,jj) )*( uc(ji-1,jj)-um(ji-1,jj) ) )
                 vpT = 0.5* ( ( vc(ji,jj)-vm(ji,jj) )*( vc(ji,jj)-vm(ji,jj) ) + ( vc(ji,jj-1)-vm(ji,jj-1) )*( vc(ji,jj-1)-vm(ji,jj-1) ) )

                 eke(ji,jj) = 0.5 * ( upT + vpT ) 
              END DO
           END DO
        ENDIF

        IF ( ltke ) THEN
           DO ji=2, npiglo
              DO jj=2,npjglo
                 ua = 0.5* ( uc(ji,jj)*uc(ji,jj) + uc(ji-1,jj)*uc(ji-1,jj) )
                 va = 0.5* ( vc(ji,jj)*vc(ji,jj) + vc(ji,jj-1)*vc(ji,jj-1) )
                 tke(ji,jj) = 0.5 * ( ua + va )
              END DO
           END DO
        ENDIF

        IF ( lmke ) THEN
           DO ji=2, npiglo
              DO jj=2,npjglo
                 rmke(ji,jj)=  0.5* (0.5*( uc(ji,jj)*uc(ji,jj) + uc(ji-1,jj)*uc(ji-1,jj)) + &
                      &              0.5*( vc(ji,jj)*vc(ji,jj) + vc(ji,jj-1)*vc(ji,jj-1)) )
              END DO
           END DO
        ENDIF

        IF ( lperio ) eke(1,:) = eke(npiglo-1,:)
        IF ( leke ) THEN 
           IF ( lperio ) eke(1,:) = eke(npiglo-1,:)
           ierr=putvar(ncout,id_varout(ip_eke), eke,  jk ,npiglo, npjglo, ktime=jt )
        ENDIF
        IF ( lmke ) THEN 
           IF ( lperio ) rmke(1,:) = rmke(npiglo-1,:)
           ierr=putvar(ncout,id_varout(ip_mke), rmke, jk ,npiglo, npjglo, ktime=jt )
        ENDIF
        IF ( ltke ) THEN 
           IF ( lperio ) tke(1,:) = tke(npiglo-1,:)
           ierr=putvar(ncout,id_varout(ip_tke), tke, jk ,npiglo, npjglo, ktime=jt )
        ENDIF

     END DO ! vertical loop
  END DO ! time loop


  ierr = closeout(ncout)

CONTAINS

  SUBROUTINE CreateOutput
    !!---------------------------------------------------------------------
    !!                  ***  ROUTINE CreateOutput  ***
    !!
    !! ** Purpose :  Create netcdf output file(s) 
    !!
    !! ** Method  :  Use stypvar global description of variables
    !!
    !!----------------------------------------------------------------------
    ip_eke = -1 ; ip_mke=-1 ;  ip_tke=-1
    stypvar(1)%ichunk = (/ npiglo, MAX(1, npjglo/30), 1, 1 /) 
    stypvar(2)%ichunk = (/ npiglo, MAX(1, npjglo/30), 1, 1 /) 
    stypvar(3)%ichunk = (/ npiglo, MAX(1, npjglo/30), 1, 1 /) 

    ivar = 1
    IF ( leke ) THEN 
       ip_eke=ivar
       ipk(ip_eke)                       = npk
       stypvar(ip_eke)%cname             = 'voeke'
       stypvar(ip_eke)%cunits            = 'm2/s2'
       stypvar(ip_eke)%rmissing_value    = 0.
       stypvar(ip_eke)%valid_min         = 0.
       stypvar(ip_eke)%valid_max         = 10000.
       stypvar(ip_eke)%clong_name        = 'Eddy_Kinetic_Energy'
       stypvar(ip_eke)%cshort_name       = 'voeke'
       stypvar(ip_eke)%conline_operation = 'N/A'
       stypvar(ip_eke)%caxis             = 'TZYX'
       ivar = ivar + 1
    ENDIF

    IF ( lmke ) THEN
       ip_mke=ivar
       ipk(ip_mke)                       = npk
       stypvar(ip_mke)%cname             = 'vomke'
       stypvar(ip_mke)%cunits            = 'm2/s2'
       stypvar(ip_mke)%rmissing_value    = 0.
       stypvar(ip_mke)%valid_min         = 0.
       stypvar(ip_mke)%valid_max         = 10000.
       stypvar(ip_mke)%clong_name        = 'Mean_Kinetic_Energy'
       stypvar(ip_mke)%cshort_name       = 'vomke'
       stypvar(ip_mke)%conline_operation = 'N/A'
       stypvar(ip_mke)%caxis             = 'TZYX'
       ivar = ivar + 1
    ENDIF

    IF ( ltke ) THEN
       ip_tke=ivar
       ipk(ip_tke)                       = npk
       stypvar(ip_tke)%cname             = 'votke'
       stypvar(ip_tke)%cunits            = 'm2/s2'
       stypvar(ip_tke)%rmissing_value    = 0.
       stypvar(ip_tke)%valid_min         = 0.
       stypvar(ip_tke)%valid_max         = 10000.
       stypvar(ip_tke)%clong_name        = 'Total_Kinetic_Energy'
       stypvar(ip_tke)%cshort_name       = 'votke'
       stypvar(ip_tke)%conline_operation = 'N/A'
       stypvar(ip_tke)%caxis             = 'TZYX'
       ivar = ivar + 1
    ENDIF


    ivar = MAX( ip_mke, ip_eke, ip_tke) ! set ivar to the effective number of variables to be output

    IF ( lsurf ) THEN
       ncout = create      (cf_out, cf_tfil, npiglo, npjglo, 0         , ld_nc4=lnc4 )
       ierr  = createvar   (ncout,  stypvar, ivar,   ipk,    id_varout , ld_nc4=lnc4 )
       ierr  = putheadervar(ncout,  cf_tfil, npiglo, npjglo, 0                       )
    ELSE
       ncout = create      (cf_out, cf_tfil, npiglo, npjglo, npk       , ld_nc4=lnc4 )
       ierr  = createvar   (ncout,  stypvar, ivar,   ipk,    id_varout , ld_nc4=lnc4 )
       ierr  = putheadervar(ncout,  cf_tfil, npiglo, npjglo, npk                     )
    ENDIF

    dtim = getvar1d(cf_ufil, cn_vtimec, npt     )
    ierr = putvar1d(ncout,  dtim,       npt, 'T')

  END SUBROUTINE CreateOutput

END PROGRAM cdfeke
