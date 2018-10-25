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

#=====//===== Checks used in this module =====//=====

def check_2D(x):
    '''
    checks the length of x if it is not 2 then 
    it exits python with a message
    '''

    if len(x) > 2:
        print '================================================='
        print 'only 2D cases are implemented with this lineshape'
        print '================================================='
        sys.exit()


def gaussian(x, intensity, loc, width):
    '''
    Gaussian line shape
    '''


    index = ((x-loc)**2.)/(2*(width**2))*(-1.)
    gauss =  np.e**(index)
    return gauss

def lorenzian(x, intensity, loc, width):
    '''
    Lorentzian line shape
    '''
    val = (loc-x)/width
    shape = 1./(1+(val**2))
    return shape

def rotatable_gauss_2D_shape(x, loc, width,theta):

    a1 = np.divide(np.cos(theta)**2.,2*(width[0]**2.))
    a2 = np.divide(np.sin(theta)**2.,2*(width[1]**2.))
    a = a1+ a2

    b1 = -1.*np.divide(np.sin(2.*theta), 4*(width[0]**2.))
    b2 = np.divide(np.sin(2.*theta), 4*(width[1]**2.))
    b = b1 + b2

    c1 = np.divide(np.sin(theta)**2.,2*(width[0]**2.))
    c2 = np.divide(np.cos(theta)**2.,2*(width[1]**2.))
    c = c1+c2

    x1 = np.ndarray.flatten(x[0])
    x2 = np.ndarray.flatten(x[1])

    model = np.zeros((len(x1), len(x2)))

    def rot_gauss(xi, yi,a,b,c, loc):

        term1 = a*(xi-loc[0])**2.
        term2 = 2*b*(xi-loc[0])*(yi-loc[1])
        term3 = c*(yi-loc[1])**2.

        index = -1.*(term1 + term2 + term3)
        
        model = (np.e**index)
        return model

    model = rot_gauss(x1[:,None], x2[None,:], a,b,c,loc)
    return model

def rotatable_lorren_2D_shape(x, loc, width,theta):

    x0_rot = loc[0]*np.cos(theta) - loc[1]*np.sin(theta)
    y0_rot = loc[0]*np.sin(theta) + loc[1]*np.cos(theta) 

    x1 = np.ndarray.flatten(x[0])
    x2 = np.ndarray.flatten(x[1])
    
    def rot_lorren(xi, yi, x0_rot, y0_rot, theta, width):

	    xi_rot = xi*np.cos(theta) - yi*np.sin(theta)
	    yi_rot = xi*np.sin(theta) + yi*np.cos(theta) 
	    

	    frac1 = (x0_rot-xi_rot)/width[0]
	    frac1 = frac1**2.
	    frac1 = 1./(1.+frac1)

	    frac2 = (y0_rot-yi_rot)/width[1]
	    frac2 = frac2**2.
	    frac2 = 1./(1.+frac2)
	    
	    return frac1*frac2
    
    return rot_lorren(x1[:,None], x2[None,:], x0_rot, y0_rot, theta, width)

def rotatable_glore_2D_shape(x, loc, width,theta, mixing):

    a1 = np.divide(np.cos(theta)**2.,2*(width[0]**2.))
    a2 = np.divide(np.sin(theta)**2.,2*(width[1]**2.))
    a = a1+ a2

    b1 = -1.*np.divide(np.sin(2.*theta), 4*(width[0]**2.))
    b2 = np.divide(np.sin(2.*theta), 4*(width[1]**2.))
    b = b1 + b2

    c1 = np.divide(np.sin(theta)**2.,2*(width[0]**2.))
    c2 = np.divide(np.cos(theta)**2.,2*(width[1]**2.))
    c = c1+c2

    x1 = np.ndarray.flatten(x[0])
    x2 = np.ndarray.flatten(x[1])

    model = np.zeros((len(x1), len(x2)))

    x0_rot = loc[0]*np.cos(theta) - loc[1]*np.sin(theta)
    y0_rot = loc[0]*np.sin(theta) + loc[1]*np.cos(theta) 

    def glore(xi, yi, x0_rot, y0_rot, theta, width, mixing):

        #lorrenzian 
        xi_rot = xi*np.cos(theta) - yi*np.sin(theta)
        yi_rot = xi*np.sin(theta) + yi*np.cos(theta) 
        
        frac1 = (x0_rot-xi_rot)/width[0]
        frac1 = frac1**2.
        frac1 = 1./(1.+frac1)

        frac2 = (y0_rot-yi_rot)/width[1]
        frac2 = frac2**2.
        frac2 = 1./(1.+frac2)
        
        lorren = frac1*frac2

        #gaussian 
        term1 = a*(xi-loc[0])**2.
        term2 = 2*b*(xi-loc[0])*(yi-loc[1])
        term3 = c*(yi-loc[1])**2.

        index = -1.*(term1 + term2 + term3)
        gauss = (np.e**index)

        return mixing*gauss + (1.-mixing)*lorren

    return glore(x1[:,None], x2[None,:], x0_rot, y0_rot, theta, width, mixing)


def rotatable_lorren_2D(x, intensity, loc, width,theta):
	check_2D(x)
	return intensity*rotatable_lorren_2D_shape(x, loc, width,theta)

def rotatable_gauss_2D(x, intensity, loc, width,theta):
	check_2D(x)
	return intensity*rotatable_gauss_2D_shape(x, loc, width,theta)

def rotatable_glore_2D(x, intensity, loc, width,theta, mixing):
    check_2D(x)
    return rotatable_glore_2D_shape(x, loc, width,theta, mixing)*intensity

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

        val = (m*gaussian(i, 1., j, k))+((1-m)*lorenzian(i, 1., j, k))
        working = working*val

    return working*intensity



