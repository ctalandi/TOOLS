
  FUNCTION lisshapiro1d(px, kiw, korder) RESULT(py)
    !!---------------------------------------------------------------------
    !!                  ***  ROUTINE lisshapiro1d  ***
    !!
    !! ** Purpose :  compute shapiro filter 
    !!
    !! References :  adapted from Mercator code
    !!----------------------------------------------------------------------
    REAL(4),    DIMENSION(:,:), INTENT(in ) :: px      ! input data
    INTEGER(4), DIMENSION(:,:), INTENT(in ) :: kiw     ! validity flags
    !REAL(4),    DIMENSION(:,:), INTENT(out) :: py      ! output data
    INTEGER(4),                 INTENT(in ) :: korder  ! order of the filter
    INTEGER(4), PARAMETER        :: kpi=1580, kpj=1801 ! size of the data

    INTEGER(4)                              :: jj, ji, jorder  ! loop indexes
    INTEGER(4)                              :: imin, imax, ihalo=0
    REAL(8), PARAMETER                      :: rp_aniso_diff_XY = 1.1 !  anisotrope case
    !REAL(8), PARAMETER                      :: rp_aniso_diff_XY = 2.25 !  anisotrope case
    REAL(8)                                 :: zalphax, zalphay, znum
    REAL(8), DIMENSION(:,:), ALLOCATABLE    :: ztmp , zpx , zpy, zkiw
    REAL(4),    DIMENSION(1580,1801)   :: py      ! output data
    LOGICAL                                      :: ll_cycl = .FALSE.
    !!----------------------------------------------------------------------

    IF(ll_cycl) ihalo=1
    ! we allocate with an ihalo
    !WRITE(*,*) 'kpi:',kpi 
    !WRITE(*,*) 'kpj:',kpj

    ALLOCATE( ztmp(0:kpi+ihalo,kpj) , zkiw(0:kpi+ihalo,kpj) )
    ALLOCATE( zpx (0:kpi+ihalo,kpj) , zpy (0:kpi+ihalo,kpj) )
    !ALLOCATE( py (kpi,kpj) )

    IF(ll_cycl) THEN
       zpx(1:kpi,:) = px(:  ,:) ;  zkiw(1:kpi,:) = kiw(:  ,:)
       zpx(0    ,:) = px(kpi,:) ;  zkiw(0    ,:) = kiw(kpi,:)
       zpx(kpi+1,:) = px(1  ,:) ;  zkiw(kpi+1,:) = kiw(1  ,:)
    ELSE
       zpx (:    ,:) = px (:  ,:)
       zkiw(:    ,:) = kiw(:  ,:)
    ENDIF

    zpy (:,:) = zpx(:,:)  ! init?
    ztmp(:,:) = zpx(:,:)  ! init

    zalphax=1./2.
    zalphay=1./2.

    !  Dx/Dy=rp_aniso_diff_XY  , D_ = vitesse de diffusion
    !  140 passes du fitre, Lx/Ly=1.5, le rp_aniso_diff_XY correspondant est:

    IF ( rp_aniso_diff_XY >=  1. ) zalphay=zalphay/rp_aniso_diff_XY
    IF ( rp_aniso_diff_XY <   1. ) zalphax=zalphax*rp_aniso_diff_XY

    DO jorder=1,korder
       WRITE(*,*) ' 	Order pass num: ', jorder
       imin = 2     - ihalo
       imax = kpi-1 + ihalo
       DO ji = imin,imax
          DO jj = 2,kpj-1
             ! We crop on the coast
             znum =    ztmp(ji,jj)                                                  &
                  &    + 0.25*zalphax*(ztmp(ji-1,jj  )-ztmp(ji,jj))*zkiw(ji-1,jj  ) &
                  &    + 0.25*zalphax*(ztmp(ji+1,jj  )-ztmp(ji,jj))*zkiw(ji+1,jj  ) &
                  &    + 0.25*zalphay*(ztmp(ji  ,jj-1)-ztmp(ji,jj))*zkiw(ji  ,jj-1) &
                  &    + 0.25*zalphay*(ztmp(ji  ,jj+1)-ztmp(ji,jj))*zkiw(ji  ,jj+1)
             zpy(ji,jj) = znum*zkiw(ji,jj)+zpx(ji,jj)*(1.-zkiw(ji,jj))
          ENDDO  ! end loop ji
       ENDDO  ! end loop jj

       IF ( ll_cycl ) THEN
          zpy(0    ,:) = zpy(kpi,:) 
          zpy(kpi+1,:) = zpy(1  ,:) 
       ENDIF

       ! update the tmp array
       ztmp(:,:) = zpy(:,:)

    ENDDO

    ! return this array
    IF( ll_cycl ) THEN
       py(:,:) = zpy(1:kpi,:)
    ELSE
       py(:,:) = zpy(:    ,:)
    ENDIF

  END FUNCTION lisshapiro1d

