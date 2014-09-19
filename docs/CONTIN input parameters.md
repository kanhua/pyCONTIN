# CONTIN input parameters

LAST
1: that last block of data
-1: not the last block of data

IUSER(4): for selecting the built-in kernel function USERK
1: For molecular weight distribution
2: diffusion coefficient distribution or Laplace transform
3: FOR SPHERICAL-RADIUS DISTRIBUTIONS
4: general form of kernel, need to modify the code of this part by the user (LINE 881)


 USERK(T,G)=FORMF2(G)*G**RUSER(23)*EXP(-RUSER(21)*T*G**RUSER(22))


 NY format:

 5100 FORMAT (1H1,9X,80A1)                                                
                                  
 5110 FORMAT (18H0(FOR ALPHA/S(1) =,1PE9.2,9H) PRUNS =,0PF7.4,9X,8HPUNCOR =,5F8.4) 

 IFORMT a user-defined format specifier (defined in the input file)


# Parameters input format
 5200 FORMAT (1X,6A1,I5,E15.6) --> This format is for parameters in input file
 5210 FORMAT (/1X,6A1,I5,1PE15.5) --> This format is for the same set of parameters in output file


Hints for inverting noisy Laplace transforms:
=============================================
With Laplace inversions, you might use the following Control 
  Parameters:
    NONNEG=T (if the solution is known to be nonnegative; without
              this constraint the resolution is extremely poor.)
    IUSER(10)=2
    GMNMX(1) about 0.1/(maximum time value in your data of 
                        signal vs. time)
    GMNMX(2) about 4/(time-spacing between data points at the 
                      shortest times)
    NG about 12*log10[GMNMX(2)/GMNMX(1)]
    IFORMY, NINTT, etc., as appropriate for your data.

The CHOSEN SOLUTION gives you a conservative (smooth) estimate 
  of a possible continuous distribution of exponentials.

The Reference Solution (the solution with the smallest ALPHA) 
  gives you the optimal analysis as a discrete sum of 
  exponentials.  The number of discrete exponentials is the 
  number of peaks.  Each amplitude is given by MOMEMT(0) for 
  the corresponding peak.  The decay rate constant is given by 
  MOMENT(1)/MOMENT(0).

Choose the solution with the smallest ALPHA that has the same 
  number of peaks as the CHOSEN SOLUTION.  This solution has 
  less smoothing bias (smaller ALPHA), but still has about 
  the same complexity (number of peaks) as the CHOSEN SOLUTION.
=================================================================