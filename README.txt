


========== Frequent Fitter ==========

This is a program that was heavily inspired by FuDA, 
a program written by Dr DF Hansen. The main drive behind
writing frequent fitter was to have a base of code I was 
familiar with and to understand the process of fitting line shapes 
to NMR peaks.

The main aim of this package is to fit NMR line shapes to 
an n-dimensional peak.

An example of the input script and a script to execute it are 
available in example/ 

Usage 
-----

To Run the program the following are needed: 

1) peaks.txt - file with the input configuration. This has the following structure: 

# name | peak possitions 1-N | line widths 1-N | radii 1-N 
dataFile | ile.ft3                                            #the NMR spectrum as a nmrPipe file
noise | 600000                                                # estimate of the noise level 
lineshape | Gauss                                             # line shape choice 
default | N/A N/A |  0.2 0.2 0.04 | 0.5 1.2  0.04             # default configurations
test1  | 47.75 17.6 0.88                                      # configurations for the specific peak

The lines for the specific peaks can be be many so long as they have different. 
The possible line shapes are: 

Line-shape   key 
Gaussian     Gauss 
Lorentzian   Loren
GLORE        Glore

The Glore function is 
f = m * Gauss() + (m-1) * Loren. 

2) To run the program one can use 
$ python runFrequentFitter.py

3) this produces a series of out put files. One is a gnuplot file 
that displays the raw data and the model. This can be plotted with 

$ gnuplot *gnu 

Install 
-------

Install this package as with any other python module. 
one possible way is: 

$ python setup.py build
$ python setup.py install 

The dependencies to run the fitting are 
- numpy
- nmrglue
- scipy
- lmfit

and gnuplot to view the fit.

If you have any questions please feel free to email me as 
Lucas.Siemons@googlemail.com

Thanks 
Lucas (author)





