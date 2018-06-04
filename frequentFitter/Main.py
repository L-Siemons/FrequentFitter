#! /usr/bin/env python
# Create a contour plot of a 2D NMRPipe spectrum

import nmrglue as ng
import numpy as np
import func
import lineShapes as ls 
import least_sq_fit as lsq
import fileIo
import lineShapeClasses as lsc


def Main(inputFile):
    print '============================'
    print '==//== FrequentFitter ==//=='
    print '- Written by Lucas Siemons -'
    print '============================'

    #read in the input file
    peaks, spec, lineshapeModel = fileIo.readInputFile(inputFile)
    #read in the spectrum 
    # read in the data from a NMRPipe file
    dic, data = ng.pipe.read(spec)
    dims = len(data.shape)
    #get the axis info
    axis = func.collect_axis(dims, dic, data)


    for peak in peaks:
        dimIndex = {}
        reducedAxis = {}
        #make the selection on the data
        #also make the selection on the axis
        for indx,(i,j) in enumerate(zip(peaks[peak]['position'], peaks[peak]['radius'])):
            dimIndex[indx] = func.get_index(i, axis[indx], j)
            reducedAxis[indx] =  axis[indx][dimIndex[indx][0]:dimIndex[indx][1]]
        

        #make the selection  
        sliceTupples =  [slice(dimIndex[a][0], dimIndex[a][1]) for a in dimIndex]
        dataReduced = data[sliceTupples]
        #apply an ellipsoid mask
        
        
        x = [ reducedAxis[i] for i in reducedAxis]
        #this is so that the function is calculated over a grid
        x = func.ndm(*x)


        result = lsq.fit(x, dataReduced, dims, lineshapeModel, peaks[peak],peak)
        result = result.params.valuesdict()

        shifts = [result['shift_%i' % (dim)] for dim in range(dims)]
        lws = [result['lw_%i' % (dim)] for dim in range(dims)]

        if lineshapeModel.mixing == False:
            models = lineshapeModel.func(x, result['intensity'], shifts, lws)
        else:
            mixing = [result['mixing_%i' % (dim)] for dim in range(dims)]
            models = lineshapeModel.func(x, result['intensity'], shifts, lws,mixing)
        #this is writing out the data
        #should be moved to another function
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

