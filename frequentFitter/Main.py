#! /usr/bin/env python
# Create a contour plot of a 2D NMRPipe spectrum

import nmrglue as ng
import numpy as np
import func
import lineShapes as ls
import least_sq_fit as lsq
import fileIo
import lineShapeClasses as lsc
import sys

def Main(inputFile):
    print '============================'
    print '==//== FrequentFitter ==//=='
    print '- Written by Lucas Siemons -'
    print '============================'

    #read in the input file
    peaks, spec, lineshapeModel, groups = fileIo.readInputFile(inputFile)
    print groups
    for i in peaks:
        check = False
        for i2 in groups:
            if i in i2:
                check = True
        if check == False:
            groups = groups + [[i]]
    print groups
    #read in the spectrum
    # read in the data from a NMRPipe file
    dic, data = ng.pipe.read(spec)
    dims = len(data.shape)

    #get the axis info
    axis = func.collect_axis(dims, dic, data)

    for group in groups:
        dimIndex = func.get_index(axis, group, peaks)

        reducedAxis = {}
        for indx in range(dims):
            reducedAxis[indx] =  axis[indx][dimIndex[indx][0]:dimIndex[indx][1]]

        #make the selection
        sliceTupples =  [slice(dimIndex[a][0], dimIndex[a][1]) for a in dimIndex]
        dataReduced = data[sliceTupples]
        #apply an ellipsoid mask

        x = [ reducedAxis[i] for i in reducedAxis]

        #this is so that the function is calculated over a grid
        x = func.ndm(*x)


        result = lsq.fit(x, dataReduced, dims, lineshapeModel, group, peaks)
        result = result.params
        models = lsq.plane(result, x, dataReduced, dims,lineshapeModel,group, peaks)

        #this is writing out the data
        #should be moved to another function
        peak = '_'.join(group)
        dataFile = peak+'.dat'
        gnuFile = peak+'.gnu'
        f = open(dataFile,'w')
        g = open(gnuFile,'w')

        counter = 0
        gnuCount = 0

        if len(dataReduced.shape) == 2:
            dataReduced = dataReduced[np.newaxis,:,:]
            models = models[np.newaxis,:,:]

        axisKeys = reducedAxis.keys()
        for sliceNum in range(dataReduced.shape[0]):
            slice_ = dataReduced[sliceNum]
            modelSlice = models[sliceNum]

            #write out the grid
            for indx1, i  in enumerate(slice_):
                for indx2, k in enumerate(slice_[indx1]):


                    co_ords = '%0.5f %0.5f' % (reducedAxis[axisKeys[-2]][indx1], reducedAxis[axisKeys[-1]][indx2])
                    res = ' %0.5f %0.5f\n' % (k, modelSlice[indx1][indx2])

                    f.write(co_ords + res)
                f.write('\n')
            f.write('\n')
            gnuCommand, gnuCount = fileIo.gnuplotCommand(gnuCount, peak ,dataFile)
            g.write(gnuCommand)
        g.close()
        f.close()

