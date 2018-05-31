import numpy as np

'''
This module contains the line shapes for the NMR signals 
In general the parameters taken are

Args: 
    x: axis
    intensity: intensity
    loc: location in each dimension (list)
    width: line width in each dimension (list)
    mixing: optional mixing term for combining multiple line shapes

Returns: 
    array: array of values taken by that line shape
'''

def gaussian(x, intensity, loc, width):
    '''
    Gaussian line shape
    '''


    index = ((x-loc)**2.)/(2*(width**2))*(-1.)
    gauss = intensity * (np.e**(index))
    return gauss

def lorenzian(x, intensity, loc, width):
    '''
    Lorentzian line shape
    '''
    val = (loc-x)/width
    shape = 1./(1+(val**2))
    return shape * intensity


def ndGaussian(x, intensity, loc, width):
    '''
    Gaussian line shape
    '''
    working = 1.


    for i,j,k in zip(x, loc, width):
        working = working*gaussian(i, 1., j, k)
    
    final = working * intensity
    return final

def ndLorentzian(x, intensity, loc, width):
    '''
    Lorentzian line shape
    '''
    working = 1.
    for i,j,k in zip(x, loc, width):
        working = working*lorenzian(i, 1., j, k)
    
    return intensity*working

def ndGlore(x, intensity, loc, width, mixing):
    '''
    Gaussian  + Lorentzian line shape
    '''
    working = 1.
    for i,j,k,m in zip(x, loc, width, mixing):
        
        val = (m*gaussian(i, 1., j, k))*((1-m)*lorenzian(i, 1., j, k))
        working = working*val

    return working*intensity