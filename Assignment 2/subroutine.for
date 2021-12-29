      program tamrin2
      implicit none
      real(8),dimension(:,:), allocatable :: bb 
      integer r,j,row
      real(8) s,n
      R=0
      OPEN(UNIT=1,FILE="input.txt",action="read",STATUS="OLD")
      do
       READ(1,*,end=1000) N 
       r=r+1
      enddo
 1000 continue
      close(1)
      allocate (bb(2,r))  
	  open(unit=10,file="input.txt",action="read",status="old")
      read (10,*)bb
      print *,bb
 
      row=r-1
      call integ(bb,s,row)
      print *,'=',s
       
       
      contains
      subroutine integ(bb,s,row)
      real(8) :: s
      integer :: row,i
      real(8):: bb(2,row)
      s=0
      do i=1,row
      s=s+(bb(1,i+1)-bb(1,i))*(exp(bb(2,i)))
      enddo
       
      end subroutine integ
      end program tamrin2



