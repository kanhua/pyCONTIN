C++++++++++++++++ DOUBLE PRECISION VERSION 2DP (MAR 1984) ++++++++++++++    2863
C  aSUBROUTINE INPUT.  READS INPUT DATA, WRITES IT OUT, AND CHECKS           2864
C      FOR INPUT ERRORS.                                                    2865
C-----------------------------------------------------------------------    2866
C  CALLS SUBPROGRAMS - STORIN, ERRMES, READYT, WRITIN                       2867
C  WHICH IN TURN CALL - USERIN, WRITYT                                      2868
C-----------------------------------------------------------------------    2869
      SUBROUTINE INPUT (EXACT,G,MA,MEQ,MG,MINEQ,MREG,MWORK,MY,SQRTW,T,Y)    2870
      DOUBLE PRECISION PRECIS, RANGE                                        2871
      LOGICAL DOCHOS, DOMOM, DOUSIN, DOUSNQ, LAST, NEWPG1,                  2872
     1 NONNEG, ONLY1, PRWT, PRY, SIMULA, LUSER                              2873
      LOGICAL LERR                                                          2874
      DIMENSION SQRTW(MY), T(MY), Y(MY), EXACT(MY), G(MG)                   2875
      DIMENSION LIN(6), LA(6,50), LA1(6,13), LA2(6,13), LA3(6,13),          2876
     1 LA4(6,11), IHOLER(6)                                                 2877
      COMMON /DBLOCK/ PRECIS, RANGE                                         2878
      COMMON /SBLOCK/ DFMIN, SRMIN,                                         2879
     1 ALPST(2), EXMAX, GMNMX(2), PLEVEL(2,2), RSVMNX(2,2), RUSER(551),     2880
     2 SRANGE                                                               2881
      COMMON /IBLOCK/ IGRID, IQUAD, IUNIT, IWT, LINEPG,                     2882
     1 MIOERR, MPKMOM, MQPITR, NEQ, NERFIT, NG, NINTT, NLINF, NORDER,       2883
     2 IAPACK(6), ICRIT(2), IFORMT(70), IFORMW(70), IFORMY(70),             2884
     3 IPLFIT(2), IPLRES(2), IPRINT(2), ITITLE(80), IUSER(50),              2885
     4 IUSROU(2), LSIGN(4,4), MOMNMX(2), NENDZ(2), NFLAT(4,2), NGL,         2886
     5 NGLP1, NIN, NINEQ, NNSGN(2), NOUT, NQPROG(2), NSGN(4), NY            2887
      COMMON /LBLOCK/ DOCHOS, DOMOM, DOUSIN, DOUSNQ, LAST,                  2888
     1 NEWPG1, NONNEG, ONLY1, PRWT, PRY, SIMULA,                            2889
     2 LUSER(30)                                                            2890
C-----------------------------------------------------------------------    2891
C  LA IS BEING BROKEN UP JUST TO KEEP THE NO. OF CONTINUATION               2892
C      CARDS IN THE DATA STATEMENTS SMALL.                                  2893
C-----------------------------------------------------------------------    2894
      EQUIVALENCE (LA(1,1),LA1(1,1)), (LA(1,14),LA2(1,1)),                  2895
     1 (LA(1,27),LA3(1,1)), (LA(1,40),LA4(1,1))                             2896
      DATA MLA/50/, IHOLER/1HI, 1HN, 1HP, 1HU, 1HT, 1H /                    2897
      DATA LA1/                                                             2898
     1 1HD, 1HF, 1HM, 1HI, 1HN, 1H ,                                        2899
     2 1HS, 1HR, 1HM, 1HI, 1HN, 1H ,   1HA, 1HL, 1HP, 1HS, 1HT, 1H ,        2900
     3 1HG, 1HM, 1HN, 1HM, 1HX, 1H ,   1HP, 1HL, 1HE, 1HV, 1HE, 1HL,        2901
     4 1HR, 1HS, 1HV, 1HM, 1HN, 1HX,   1HR, 1HU, 1HS, 1HE, 1HR, 1H ,        2902
     5 1HI, 1HG, 1HR, 1HI, 1HD, 1H ,   1HI, 1HQ, 1HU, 1HA, 1HD, 1H ,        2903
     6 1HI, 1HU, 1HN, 1HI, 1HT, 1H ,   1HI, 1HW, 1HT, 3*1H ,                2904
     7 1HL, 1HI, 1HN, 1HE, 1HP, 1HG,   1HM, 1HI, 1HO, 1HE, 1HR, 1HR/        2905
      DATA LA2/                                                             2906
     1 1HM, 1HP, 1HK, 1HM, 1HO, 1HM,   1HM, 1HQ, 1HP, 1HI, 1HT, 1HR,        2907
     2 1HN, 1HE, 1HQ, 3*1H ,           1HN, 1HE, 1HR, 1HF, 1HI, 1HT,        2908
     3 1HN, 1HG, 4*1H ,                1HN, 1HI, 1HN, 1HT, 1HT, 1H ,        2909
     4 1HN, 1HL, 1HI, 1HN, 1HF, 1H ,   1HN, 1HO, 1HR, 1HD, 1HE, 1HR,        2910
     5 1HI, 1HC, 1HR, 1HI, 1HT, 1H ,                                        2911
     6 1HI, 1HF, 1HO, 1HR, 1HM, 1HT,   1HI, 1HF, 1HO, 1HR, 1HM, 1HW,        2912
     7 1HI, 1HF, 1HO, 1HR, 1HM, 1HY,   1HI, 1HP, 1HL, 1HF, 1HI, 1HT/        2913
      DATA LA3/                                                             2914
     1 1HI, 1HP, 1HL, 1HR, 1HE, 1HS,   1HI, 1HP, 1HR, 1HI, 1HN, 1HT,        2915
     2 1HI, 1HU, 1HS, 1HE, 1HR, 1H ,   1HI, 1HU, 1HS, 1HR, 1HO, 1HU,        2916
     3 1HL, 1HS, 1HI, 1HG, 1HN, 1H ,   1HM, 1HO, 1HM, 1HN, 1HM, 1HX,        2917
     4 1HN, 1HE, 1HN, 1HD, 1HZ, 1H ,   1HN, 1HF, 1HL, 1HA, 1HT, 1H ,        2918
     5 1HN, 1HN, 1HS, 1HG, 1HN, 1H ,   1HN, 1HQ, 1HP, 1HR, 1HO, 1HG,        2919
     6 1HN, 1HS, 1HG, 1HN, 2*1H ,      1HD, 1HO, 1HC, 1HH, 1HO, 1HS,        2920
     7 1HD, 1HO, 1HM, 1HO, 1HM, 1H /                                        2921
      DATA LA4/                                                             2922
     1 1HD, 1HO, 1HU, 1HS, 1HI, 1HN,   1HD, 1HO, 1HU, 1HS, 1HN, 1HQ,        2923
     2 1HL, 1HA, 1HS, 1HT, 2*1H ,      1HN, 1HE, 1HW, 1HP, 1HG, 1H1,        2924
     3 1HN, 1HO, 1HN, 1HN, 1HE, 1HG,   1HO, 1HN, 1HL, 1HY, 1H1, 1H ,        2925
     4 1HP, 1HR, 1HW, 1HT, 2*1H ,      1HP, 1HR, 1HY, 3*1H ,                2926
     5 1HS, 1HI, 1HM, 1HU, 1HL, 1HA,   1HL, 1HU, 1HS, 1HE, 1HR, 1H ,        2927
     6 1HE, 1HN, 1HD, 3*1H /                                                2928
 5100 FORMAT (80A1)                                                         2929
      READ (NIN,5100) ITITLE                                                2930
 5999 FORMAT (1H1)                                                          2931
      IF (NEWPG1) WRITE (NOUT,5999)                                         2932
 5101 FORMAT (34H CONTIN - VERSION 2DP (MAR 1984) (,6A1,6H PACK),6X,80A1    2933
     1 //59H REFERENCES - S.W. PROVENCHER (1982) COMPUT. PHYS. COMMUN.,,    2934
     2 33H VOL. 27, PAGES 213-227, 229-242./30X,                            2935
     3 53H(1984) EMBL TECHNICAL REPORT DA07 (EUROPEAN MOLECULAR,            2936
     4 49H BIOLOGY LABORATORY, HEIDELBERG, F.R. OF GERMANY)                 2937
     5 ///20X,42HINPUT DATA FOR CHANGES TO COMMON VARIABLES)                2938
      WRITE (NOUT,5101) IAPACK, ITITLE                                      2939
      NIOERR=0                                                              2940
 5200 FORMAT (1X,6A1,I5,E15.6)                                              2941
  200 READ (NIN,5200) LIN,IIN,RIN                                           2942
 5210 FORMAT (/1X,6A1,I5,1PE15.5)                                           2943
      WRITE (NOUT,5210) LIN,IIN,RIN                                         2944
      DO 210 J=1,MLA                                                        2945
        DO 220 K=1,6                                                        2946
          IF (LIN(K) .NE. LA(K,J)) GO TO 210                                2947
  220   CONTINUE                                                            2948
        IF (J .EQ. MLA) GO TO 300                                           2949
        JJ=J                                                                2950
        CALL STORIN (JJ,NIOERR,LIN,IIN,RIN)                                 2951
        GO TO 200                                                           2952
  210 CONTINUE                                                              2953
      CALL ERRMES (1,.FALSE.,IHOLER,NOUT)                                   2954
 5001 FORMAT (1H )                                                          2955
      WRITE (NOUT,5001)                                                     2956
      NIOERR=NIOERR+1                                                       2957
      IF (NIOERR .GE. MIOERR) STOP                                          2958
      GO TO 200                                                             2959
  300 CALL READYT (MY,NIOERR,SQRTW,T,Y)                                     2960
      CALL WRITIN (EXACT,G,LA,MG,MY,SQRTW,T,Y)                              2961
      NEWPG1=.TRUE.                                                         2962
C-----------------------------------------------------------------------    2963
C  CHECK COMMON VARIABLES FOR VIOLATIONS.                                   2964
C-----------------------------------------------------------------------    2965
      LERR=.FALSE.                                                          2966
      DO 410 K=1,2                                                          2967
        DO 420 J=1,2                                                        2968
          IF (K.EQ.2 .OR. (IWT.NE.1 .AND. IWT.NE.4)) LERR=LERR .OR.         2969
     1    PLEVEL(J,K).LT.0. .OR. PLEVEL(J,K).GT.1. .OR. ICRIT(K).LT.1       2970
     2     .OR. ICRIT(K).GT.2                                               2971
  420   CONTINUE                                                            2972
        IF (NQPROG(1) .GT. 0) LERR=LERR .OR. RSVMNX(K,1).LE.0.              2973
  410 CONTINUE                                                              2974
      LERR=LERR .OR. MIN0(IGRID,IQUAD,IWT,NG-1,NG+NLINF-NEQ).LT.1 .OR.      2975
     1 MIN0(NLINF,NEQ).LT.0 .OR.                                            2976
     2 MAX0(IGRID-3,IQUAD-3,IWT-5,NEQ-MEQ,NG+NLINF+2-MIN0(MG,MA),           2977
     3 NG+NLINF+1-MREG,NORDER-5,                                            2978
     4 MAX0(MG,NY)-MY,MAX0((MINEQ+2)*(MG+1)-4,MG*(MG-2),4*MG)-MWORK)        2979
     5 .GT. 0                                                               2980
      IF (.NOT.LERR) GO TO 500                                              2981
      CALL ERRMES (2,.FALSE.,IHOLER,NOUT)                                   2982
 5420 FORMAT (5H MY =,I5,5X,4HMA =,I3,5X,4HMG =,I3,5X,6HMREG =,I3,5X,       2983
     1 7HMINEQ =,I3,5X,5HMEQ =,I3,5X,7HMWORK =,I5)                          2984
      WRITE (NOUT,5420) MY,MA,MG,MREG,MINEQ,MEQ,MWORK                       2985
      STOP                                                                  2986
  500 IF (NIOERR .NE. 0) STOP                                               2987
      RETURN                                                                2988
      END                                                                   2989


C++++++++++++++++ DOUBLE PRECISION VERSION 2DP (MAR 1984) ++++++++++++++    4263
C  aSUBROUTINE READYT.  READS Y(J) (INPUT DATA), T(J) (INDEPENDENT           4264
C      VARIABLE), AND, IF IWT=4, LEAST SQUARES WEIGHTS, FOR J=1,NY.         4265
C  IF DOUSIN=.TRUE., THEN USERIN IS CALLED TO RECOMPUTE OR CHANGE           4266
C      INPUT DATA.                                                          4267
C-----------------------------------------------------------------------    4268
C  CALL SUBPROGRAMS - USERIN, ERRMES                                        4269
C-----------------------------------------------------------------------    4270
      SUBROUTINE READYT (MY,NIOERR,SQRTW,T,Y)                               4271
      DOUBLE PRECISION PRECIS, RANGE                                        4272
      LOGICAL DOCHOS, DOMOM, DOUSIN, DOUSNQ, LAST, NEWPG1,                  4273
     1 NONNEG, ONLY1, PRWT, PRY, SIMULA, LUSER                              4274
      DIMENSION SQRTW(MY), T(MY), Y(MY)                                     4275
      DIMENSION LIN(6), LA(6,2), IHOLER(6)                                  4276
      COMMON /DBLOCK/ PRECIS, RANGE                                         4277
      COMMON /SBLOCK/ DFMIN, SRMIN,                                         4278
     1 ALPST(2), EXMAX, GMNMX(2), PLEVEL(2,2), RSVMNX(2,2), RUSER(551),     4279
     2 SRANGE                                                               4280
      COMMON /IBLOCK/ IGRID, IQUAD, IUNIT, IWT, LINEPG,                     4281
     1 MIOERR, MPKMOM, MQPITR, NEQ, NERFIT, NG, NINTT, NLINF, NORDER,       4282
     2 IAPACK(6), ICRIT(2), IFORMT(70), IFORMW(70), IFORMY(70),             4283
     3 IPLFIT(2), IPLRES(2), IPRINT(2), ITITLE(80), IUSER(50),              4284
     4 IUSROU(2), LSIGN(4,4), MOMNMX(2), NENDZ(2), NFLAT(4,2), NGL,         4285
     5 NGLP1, NIN, NINEQ, NNSGN(2), NOUT, NQPROG(2), NSGN(4), NY            4286
      COMMON /LBLOCK/ DOCHOS, DOMOM, DOUSIN, DOUSNQ, LAST,                  4287
     1 NEWPG1, NONNEG, ONLY1, PRWT, PRY, SIMULA,                            4288
     2 LUSER(30)                                                            4289
      DATA IHOLER/1HR, 1HE, 1HA, 1HD, 1HY, 1HT/, LA/                        4290
     1 1HN, 1HS, 1HT, 1HE, 1HN, 1HD,   1HN, 1HY, 4*1H /                     4291
      IF (NINTT .LE. 0) GO TO 200                                           4292
C-----------------------------------------------------------------------    4293
C  COMPUTE T IN EQUAL INTERVALS.                                            4294
C-----------------------------------------------------------------------    4295
      NY=0                                                                  4296
      DO 110 J=1,NINTT                                                      4297
 5110 FORMAT (1X,6A1,I5,2E15.6)                                             4298
      READ (NIN,5110) LIN,NT,TSTART,TEND                                    4299
 5120 FORMAT (1X,6A1,I5,1P2E15.5)                                           4300
      WRITE (NOUT,5120) LIN,NT,TSTART,TEND                                  4301
      DO 120 K=1,6                                                          4302
        IF (LIN(K) .NE. LA(K,1)) GO TO 130                                  4303
  120 CONTINUE                                                              4304
      GO TO 140                                                             4305
  130 CALL ERRMES (1,.FALSE.,IHOLER,NOUT)                                   4306
      GO TO 190                                                             4307
  140 IF (NT.GE.2 .AND. NT+NY.LE.MY) GO TO 150                              4308
      CALL ERRMES (2,.FALSE.,IHOLER,NOUT)                                   4309
      GO TO 190                                                             4310
  150 DUM=(TEND-TSTART)/FLOAT(NT-1)                                         4311
      NY=NY+1                                                               4312
      T(NY)=TSTART                                                          4313
      DO 160 K=2,NT                                                         4314
      NY=NY+1                                                               4315
  160 T(NY)=T(NY-1)+DUM                                                     4316
      GO TO 110                                                             4317
  190 NIOERR=NIOERR+1                                                       4318
      IF (NIOERR .GE. MIOERR) STOP                                          4319
  110 CONTINUE                                                              4320
      GO TO 300                                                             4321
C-----------------------------------------------------------------------    4322
C  READ IN NY AND THEN T ARRAY.                                             4323
C-----------------------------------------------------------------------    4324
  200 READ (NIN,5110) LIN,NY                                                4325
      WRITE (NOUT,5110) LIN,NY                                              4326
      DO 210 K=1,6                                                          4327
        IF (LIN(K) .NE. LA(K,2)) GO TO 220                                  4328
  210 CONTINUE                                                              4329
      GO TO 230                                                             4330
  220 CALL ERRMES (3,.FALSE.,IHOLER,NOUT)                                   4331
      GO TO 235                                                             4332
  230 IF (NY .LE. MY) GO TO 240                                             4333
      CALL ERRMES (4,.FALSE.,IHOLER,NOUT)                                   4334
  235 NIOERR=NIOERR+1                                                       4335
      RETURN                                                                4336
  240 READ (NIN,IFORMT) (T(J),J=1,NY)                                       4337
C-----------------------------------------------------------------------    4338
C  READ IN Y ARRAY.                                                         4339
C-----------------------------------------------------------------------    4340
  300 IF (.NOT.SIMULA) READ (NIN,IFORMY) (Y(J),J=1,NY)                      4341
      IF (IWT .EQ. 4) GO TO 420                                             4342
C-----------------------------------------------------------------------    4343
C  INITIALIZE SQRTW (SQUARE ROOTS OF LEAST SQUARES WEIGHTS) TO UNITY.       4344
C-----------------------------------------------------------------------    4345
      DO 410 J=1,NY                                                         4346
      SQRTW(J)=1.                                                           4347
  410 CONTINUE                                                              4348
C-----------------------------------------------------------------------    4349
C  READ IN LEAST SQUARES WEIGHTS IF IWT=4.                                  4350
C-----------------------------------------------------------------------    4351
  420 IF (IWT .EQ. 4) READ (NIN,IFORMW) (SQRTW(J),J=1,NY)                   4352
C-----------------------------------------------------------------------    4353
C  CALL USERIN TO CHANGE OR RECOMPUTE INPUT DATA.                           4354
C-----------------------------------------------------------------------    4355
      IF (DOUSIN) CALL USERIN (T,Y,SQRTW,MY)                                4356
      DO 430 J=1,NY                                                         4357
      IF (SQRTW(J) .GE. 0.) GO TO 440                                       4358
      CALL ERRMES (5,.FALSE.,IHOLER,NOUT)                                   4359
 5440 FORMAT (1X,1P10E13.5)                                                 4360
      WRITE (NOUT,5440) (SQRTW(K),K=1,NY)                                   4361
      NIOERR=NIOERR+1                                                       4362
      GO TO 800                                                             4363
  440 SQRTW(J)=SQRT(SQRTW(J))                                               4364
  430 CONTINUE                                                              4365
  800 RETURN                                                                4366
      END                                                                   4367