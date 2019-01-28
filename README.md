# pyCONTIN package:
This is a python wrapper for CONTIN package.
CONTIN package is a Fortran77 program for solving Fredelhom equations of the first kind, developed by S.W. Provencher.

Currently this wrapper generates the input file for CONTIN main program, and then parse the output of the CONTIN main program.

[Official webpage of CONTIN](http://lcmodel.ca/contin.shtml)

## How does the program work

### input for pyCONTIN
- Data to be analyzed
- Parameter file for CONTIN

### The process
1. The program reads the data and the parameter file, then it generates input files for CONTIN fortran program. 
2. CONTIN does the calculation and returns the results in an ouput file.
3. pyCONTIN parse the output file and returns the result

## Files required to run this program
```./dev/CONTINWrapper.py```: Main script of pyCONTIN. Only this file, this file does not depend on other python files in this script. Most of the python files in this package are just test files.

```./exec/contin.for```: The main program of doing inverse Laplace transform

```./dev/paramTemplate.txt```: A parameter file set up by the user for setting the parameters of CONTIN.


## Installation and setup
- Install gfortran for your system
- In ```./exec``` folder, run the following command to  

```
gfortran -std=legacy contin.for -o contin.out
```
- Change ```CONTINPath``` variable at the beginning of ```CONTINWrapper.py``` to the path your fortran executable ```contin.out```. The path can be set as the relative path to the path of ```CONTINWrapper.py```

At the moment, this program only supports python 2.7


## Usage

The calculated results in the ouput file of CONTIN looks like this:

```
      ALPHA    ALPHA/S(1)     OBJ. FCTN.       VARIANCE      STD. DEV.    DEG FREEDOM    PROB1 TO REJECT    PROB2 TO REJECT
 * 6.11E-08      8.02E-13    9.83727E+00    9.83727E+00      9.923E-02          1.000              0.000              1.000

    ORDINATE    ERROR  ABSCISSA
   0.000E+00  5.5D-19  5.00E-06X                                                                                                   
   0.000E+00  4.2D-17  7.12E-06X                                                                                                   
   0.000E+00  7.1D-17  1.01E-05X                                                                                                   
   0.000E+00  1.1D-17  1.44E-05X 


```

PyCONTIN parses these output blocks and returns a list of tuples like this:

```
[[(alphaParam1, dataArray1), (alphaParam2,dataArray2),....]
```
```alphaParam``` records the row next to ```ALPHA    ALPHA/S(1)     OBJ. FCTN. ...```
```dataArray``` records the three column data after ```   ORDINATE    ERROR  ABSCISSA```

For example script, see ```./dev/pyCONTIN_demo.py```

