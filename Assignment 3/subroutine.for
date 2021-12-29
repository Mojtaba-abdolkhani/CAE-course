      SUBROUTINE FILM(H,SINK,TEMP,KSTEP,KINC,TIME,NOEL,NPT,
     1COORDS,JLTYP,FIELD,NFIELD,SNAME,NODE,AREA)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION H(2),TIME(2),COORDS(3), FIELD(NFIELD)
      CHARACTER*80 SNAME
      PARAMETER (two=2.0D0,third=1.0D0/3.0D0)
	  Aa=1.0D0
	  SINK=100.0D0
	  al=SIGN(Aa,TEMP-SINK)
	  H(1)=500.0D0*(ABS(TEMP-SINK))**third
	  H(2) = al*third*500.0d0*(abs(temp-sink))**(-two*third) 
   	 
     

      RETURN
      END
      	  