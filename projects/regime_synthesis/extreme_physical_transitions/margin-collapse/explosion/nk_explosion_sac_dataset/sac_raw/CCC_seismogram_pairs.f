c        1         2         3         4         5         6         7
c23456789012345678901234567890123456789012345678901234567890123456789012
c

      parameter(npts0=180000,nsta0=50)
      character*180 inlist1,inlist2,sacfile,outfile
      character*8 kstnm,kcmpnm,knetwk
      character*8 net1(nsta0),sname1(nsta0),cname1(nsta0)
      character*8 net2(nsta0),sname2(nsta0),cname2(nsta0)
      real yarray(npts0),dt1(nsta0),dt2(nsta0),beg,stla,stlo,tbuff
      real slat1(nsta0),slon1(nsta0),amp1(npts0,nsta0),tdif1(nsta0)
      real slat2(nsta0),slon2(nsta0),amp2(npts0,nsta0),tdif2(nsta0)
      real y1(npts0),y2(npts0)
      real fdel1(nsta0),fdel2(nsta0),fazi1(nsta0),fazi2(nsta0)
      real*8 toff8
      integer npts1(nsta0),npts2(nsta0)

      print *,'Enter input saclist for reference event (#1)'
      read (*,'(a)') inlist1

      print *,'Enter input saclist for event to be rel. located (#2)'
      read (*,'(a)') inlist2

      print *,'Enter event1: yr mon dy hr min sec'
      read *,iqyr1,iqmon1,iqday1,iqhr1,iqmn1,fqsc1

      print *,'Enter event2: yr mon dy hr min sec'
      read *,iqyr2,iqmon2,iqday2,iqhr2,iqmn2,fqsc2

      print *,'Enter master Lat Lon'
      read *,reflat,reflon

      print *,'XCOR window before after shift e.g.:  -4 10 3'
      read *,tbefore,tafter,tshift

      print *,'Velocity'
      read *,fvel

      print *,'Enter output file name'
      read (*,'(a)') outfile

c----------------- read in sac files --------------------

101   format(a180)

      open(4,file=inlist1)
      do i=1,nsta0
         read(4,101,end=201) sacfile
         call RSAC1(sacfile,yarray,npts1(i),beg,
     &              dt1(i),npts0,NERR)
         CALL GETKHV('kstnm',kstnm,NERR0)
         sname1(i)(1:6)=kstnm(1:6)
         CALL GETKHV('kcmpnm',kcmpnm,NERR1)
         cname1(i)(1:3)=kcmpnm(1:3)
         CALL GETKHV('knetwk',knetwk,NERR2)
         net1(i)(1:2)=knetwk(1:2)
         CALL GETFHV('stla',stla,NERR3)
         slat1(i)=stla
         CALL GETFHV('stlo',stlo,NERR4)
         slon1(i)=stlo
         call SPH_AZI(reflat,reflon,stla,stlo,fdel,fazi)
         fdel1(i)=fdel
         fazi1(i)=fazi
         CALL GETNHV('nzyear',nzyear,NERR5)
         CALL GETNHV('nzjday',nzjday,NERR5)
         CALL GETNHV('nzhour',nzhour,NERR5)
         CALL GETNHV('nzmin',nzmin,NERR5)
         CALL GETNHV('nzsec',nzsec,NERR5)
         CALL GETNHV('nzmsec',nzmsec,NERR5)
         call DT_GET_DAY(nzyear,nzjday,nzmon,nzday)
         f2=(nzsec*1.)+(nzmsec/1000.)
         call DT_TIMEDIF(iqyr1,iqmon1,iqday1,iqhr1,iqmn1,fqsc1,
     &                   nzyear,nzmon,nzday,nzhour,
     &                   nzmin,f2,toff8)
         tdif1(i)=toff8*1.
         fmax=0.
         do j=1,npts1(i)
            if (abs(yarray(j)).gt.fmax) fmax=abs(yarray(j))
         enddo
         do j=1,npts1(i)
            amp1(j,i)=yarray(j)/fmax
         enddo

        print *,i,dt1(i),tdif1(i),fdel1(i),fazi1(i)

      enddo   !------ do i=1,nsta0
201   close(4)
      nseis1=i-1

c----------------- read in sac files --------------------

      open(4,file=inlist2)
      do i=1,nsta0
         read(4,101,end=202) sacfile
         call RSAC1(sacfile,yarray,npts2(i),beg,
     &              dt2(i),npts0,NERR)
         CALL GETKHV('kstnm',kstnm,NERR0)
         sname2(i)(1:6)=kstnm(1:6)
         CALL GETKHV('kcmpnm',kcmpnm,NERR1)
         cname2(i)(1:3)=kcmpnm(1:3)
         CALL GETKHV('knetwk',knetwk,NERR2)
         net2(i)(1:2)=knetwk(1:2)
         CALL GETFHV('stla',stla,NERR3)
         slat2(i)=stla
         CALL GETFHV('stlo',stlo,NERR4)
         slon2(i)=stlo
         call SPH_AZI(reflat,reflon,stla,stlo,fdel,fazi)
         fdel2(i)=fdel
         fazi2(i)=fazi
         CALL GETNHV('nzyear',nzyear,NERR5)
         CALL GETNHV('nzjday',nzjday,NERR5)
         CALL GETNHV('nzhour',nzhour,NERR5)
         CALL GETNHV('nzmin',nzmin,NERR5)
         CALL GETNHV('nzsec',nzsec,NERR5)
         CALL GETNHV('nzmsec',nzmsec,NERR5)
         call DT_GET_DAY(nzyear,nzjday,nzmon,nzday)
         f2=(nzsec*1.)+(nzmsec/1000.)
         call DT_TIMEDIF(iqyr2,iqmon2,iqday2,iqhr2,iqmn2,fqsc2,
     &                   nzyear,nzmon,nzday,nzhour,
     &                   nzmin,f2,toff8)
         tdif2(i)=toff8*1.
         fmax=0.
         do j=1,npts2(i)
            if (abs(yarray(j)).gt.fmax) fmax=abs(yarray(j))
         enddo
         do j=1,npts2(i)
            amp2(j,i)=yarray(j)/fmax
         enddo

        print *,i,dt2(i),tdif2(i),fdel2(i),fazi2(i)

      enddo   !------ do i=1,nsta0
202   close(4)
      nseis2=i-1

c---------- do some cross-correlations -------------------

      nxcor=nint((tafter-tbefore)/dt1(1))
      nshift=nint(tshift/dt1(1))
      iadd=nint((7.+tafter-tbefore)/dt1(1))

        print *,'nseis ',nseis1,nseis2

      open(4,file=outfile,recl=4096)
      do i1=1,nseis1
         do i2=1,nseis2
            if (sname1(i1)(1:4).eq.sname2(i2)(1:4)) then
               tadd=(fdel1(i1)*111.19/fvel)-tbefore
               iref1=nint((tadd-tdif1(i1))/dt1(i1))
               iref2=nint((tadd-tdif2(i2))/dt2(i2))
               npts=min(npts1(i1),npts2(i2))
               do j=1,npts
                  y1(j)=amp1(j,i1)
                  y2(j)=amp2(j,i2)
               enddo
               call GETXCOR_EASY(y1,y2,npts,iref1,iref2,nxcor,
     &                           nshift,rmax,ir1,rmin,ir2)
               print *,sname1(i1)(1:4),' ',rmax,ir1

               iref1=nint((tadd-tdif1(i1)-5.)/dt1(i1))
               iref2=nint((tadd-tdif2(i2)-5.)/dt2(i2))
               fmax1=0.
               fmax2=0.
               do j=iref1,iref1+iadd
                  if (abs(y1(j)).gt.fmax1) fmax1=abs(y1(j))
                  if (abs(y2(j)).gt.fmax2) fmax2=abs(y2(j))
               enddo
               time=-5.
               do j1=iref1,iref1+iadd
                  time=time+dt1(1)
                  write(4,*)i1,time,y1(j1)/fmax1,y2(j1)/fmax2,
     &                      ir1*dt1(i1),rmax,fazi1(i1)
               enddo
            endif
         enddo
      enddo
      close(4)

      end




c--------------------------------------------------------------------------
c--------------------------------------------------------------------------
c--------------------------------------------------------------------------

      subroutine GETXCOR_EASY(a1,a2,n,iref1,iref2,nxcor,
     &              nshift,rmax,ir1,rmin,ir2)
      real a1(n),a2(n),xcor
      rmax=-1.
      rmin=1.

      do 100 ishift=-nshift,nshift
         ishifta=ishift/2
         ishiftb=ishift-ishifta
         suma=0.
         sumb=0.
         sumab=0.
         do 60 ixcor=0,nxcor
            ita=iref1+ixcor-ishifta
            itb=iref2+ixcor+ishiftb
            suma=suma+a1(ita)**2
            sumb=sumb+a2(itb)**2
            sumab=sumab+a1(ita)*a2(itb)
60       continue
         denom=suma*sumb
         sdenom=sqrt(denom)
         if (sdenom.ne.0.) then
            test=sumab/sdenom
         else
            go to 100
         end if
         if (test.gt.rmax) then
            rmax=test
            ir1=ishift
         end if
         if (test.lt.rmin) then
            rmin=test
            ir2=ishift
         end if
100   continue
      return
      end


c SPH_AZI computes distance and azimuth between two points on sphere
c
c Inputs:  flat1  =  latitude of first point (degrees) 
c          flon2  =  longitude of first point (degrees)
c          flat2  =  latitude of second point (degrees)
c          flon2  =  longitude of second point (degrees)
c Returns: del    =  angular separation between points (degrees)
c          azi    =  azimuth at 1st point to 2nd point, from N (deg.)
c
c Note:  This routine is inaccurate for del less than about 0.5 degrees. 
c        For greater accuracy, use SPH_AZIDP or perform a separate
c        calculation for close ranges using Cartesian geometry.
c
      subroutine SPH_AZI(flat1,flon1,flat2,flon2,del,azi)
      if ((flat1.eq.flat2.and.flon1.eq.flon2).or.
     &    (flat1.eq.90..and.flat2.eq.90.).or.
     &    (flat1.eq.-90..and.flat2.eq.-90.))  then
         del=0.
         azi=0.
         return
      end if
      pi=3.141592654
      raddeg=pi/180.
      theta1=(90.-flat1)*raddeg
      theta2=(90.-flat2)*raddeg
      phi1=flon1*raddeg
      phi2=flon2*raddeg
      stheta1=sin(theta1)
      stheta2=sin(theta2)
      ctheta1=cos(theta1)
      ctheta2=cos(theta2)
      cang=stheta1*stheta2*cos(phi2-phi1)+ctheta1*ctheta2
      ang=acos(cang)
      del=ang/raddeg
      sang=sqrt(1.-cang*cang)
      caz=(ctheta2-ctheta1*cang)/(sang*stheta1)
      saz=-stheta2*sin(phi1-phi2)/sang
      az=atan2(saz,caz)
      azi=az/raddeg
      if (azi.lt.0.) azi=azi+360.
      return
      end


c DT_GET_DAY gets standard (month, day) from (year, Julian day)
c   Example: 1999, 105 gives 4, 15
c
c Inputs:  iyear  =  year (4 digits)
c          jday   =  Julian day (1 to 366)
c Returns: imon   =  month (1 to 12)
c          iday   =  day
c
      subroutine DT_GET_DAY(iyear,jday,imon,iday)
      integer jsum(12),jsum2(12)
      logical leapyear
      data jsum/ 0,31,59,90,120,151,181,212,243,273,304,334/
      data jsum2/0,31,60,91,121,152,182,213,244,274,305,335/
      if (mod(iyear,400).eq.0) then       !leap year
         leapyear=.true.
      else if (mod(iyear,100).eq.0) then  !not a leap year
         leapyear=.false.
      else if (mod(iyear,4).eq.0) then    !leap year
         leapyear=.true.
      else                                !not a leap year
         leapyear=.false.
      end if
      if (leapyear) then
         do 10 i=2,12
            if (jsum2(i).ge.jday) then
               iday=jday-jsum2(i-1)
               imon=i-1
               return
            end if
10       continue
         iday=jday-jsum2(12)
         imon=12
      else
         do 20 i=2,12
            if (jsum(i).ge.jday) then
               iday=jday-jsum(i-1)
               imon=i-1
               return
            end if
20       continue
         iday=jday-jsum(12)
         imon=12
      end if
      return
      end


c DT_TIMEDIF finds time difference between two date/times
c
c Inputs:  iyr1,imon1,idy1,ihr1,imn1,sc1  =  1st year,mon,day,hour,min,sec
c          iyr2,imon2,idy2,ihr2,imn2,sc2  =  2nd year,mon,day,hour,min,sec 
c Returns: timdif  =  2nd - 1st time (real*8 seconds)
c
c Note:  timdif is real*8, sc1,sc2 are real*4, other I/O are integers
c
      subroutine DT_TIMEDIF(iyr1,imon1,idy1,ihr1,imn1,sc1,
     &                      iyr2,imon2,idy2,ihr2,imn2,sc2,timdif)
      real*8 timdif
      call DT_GET_TDAY(iyr1,imon1,idy1,itday1)
      call DT_GET_TDAY(iyr2,imon2,idy2,itday2)
      timdif =  dble(3600.)*dble(ihr2-ihr1)
     &         +dble(  60.)*dble(imn2-imn1)+dble(sc2-sc1)
      timdif=timdif+dble(86400.)*dble(itday2-itday1)
      return
      end


c DT_GET_TDAY gets total number of days since 0 Jan 1600
c   Example: 1999,3,13 gives 145803
c
c Inputs:  iyear  =  year (4 digits)
c          imon   =  month (1 to 12)
c          iday   =  day (1 to 31)
c Returns: itday  =  days from 0 Jan 1600
c
      subroutine DT_GET_TDAY(iyear,imon,iday,itday)
      call DT_GET_JDAY(iyear,imon,iday,jday)
      itday=(iyear-1600)*365+jday
      itday=itday+int((iyear-1601)/4)    !add mult 4 LY
      itday=itday-int((iyear-1601)/100)  !subtract mult 100 lack of LY
      itday=itday+int((iyear-1601)/400)  !add mult 400 LY
      return
      end


c DT_GET_JDAY gets Julian day from (year, month, day)
c   Example: 1999, 4, 15 gives 105
c
c Inputs:  iyear  =  year (4 digits)
c          imon   =  month (1 to 12)
c          iday   =  day
c Returns: jday   =  Julian day (1 to 366)
c
      subroutine DT_GET_JDAY(iyear,imon,iday,jday)
      integer jsum(12),jsum2(12)
      data jsum/ 0,31,59,90,120,151,181,212,243,273,304,334/
      data jsum2/0,31,60,91,121,152,182,213,244,274,305,335/
      if (mod(iyear,400).eq.0) then       !leap year
         jday=jsum2(imon)+iday
      else if (mod(iyear,100).eq.0) then  !not a leap year
         jday=jsum(imon)+iday
      else if (mod(iyear,4).eq.0) then    !leap year
         jday=jsum2(imon)+iday
      else                                !not a leap year
         jday=jsum(imon)+iday
      end if
      return
      end


