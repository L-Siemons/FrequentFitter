import numpy as np
import scipy
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
import lineShapes as ls
import fileIo


def residual(params, x, data, dims,lineShape,start,mixingState):
    '''
    this works out the residual

    Args:
        params: lmfit object containing values to be fitted
        x: axis  
        dims: dimensions 
        lineShape: class describing the line shape 
        mixingState: boolean for if the line shaoe is a combination
    Returns: 
        Chi-square: float
    '''
    
    shifts = [params['shift_%i' % (dim)] for dim in range(dims)]
    lws = [params['lw_%i' % (dim)] for dim in range(dims)]

    if mixingState == False:
        model = lineShape.func(x, params['intensity'], shifts, lws)
    else:
    	mixing = [params['mixing_%i' % (dim)] for dim in range(dims)]
        model = lineShape.func(x, params['intensity'], shifts, lws, mixing)

    return (data - model)/start['noise']

def setup_params(dims, lineShape,start):
    '''
    Set up the parameters object from lmfit
    
    Args:
        dims: number of dimensions 
        lineshape: class describing the line shape 
        start: dictionary containing the start parameters
    
    Returns:
        params: lmfit Parameters() class
    '''
    #define parameters
    params = Parameters()
    
    for i,(j,k) in enumerate(zip(start['position'], start['lw'])):
        lw_tag = 'lw_%i'%(i)
        shift_tag = 'shift_%i'%(i)
        params.add(lw_tag, vary=False, value=k, min=0)
        params.add(shift_tag, vary=False, value=j)
        
        if lineShape.mixing == True:
        	mixing_tag = 'mixing_%i'%(i)
        	params.add(mixing_tag, vary=False, value=0.2, min=0, max=1)
        

    params.add('intensity',vary=False,value=start['intensity'])
    return params

def fit(x, data, dims, lineShape, start,name):

    '''
    This function carries out the least squares fitting. 
    The fitting proceeds in three steps. The parameters 
    fitted in each step are defined in the lineShape classes. 

    In general terms the steps are as follows: 
    1) fit line width and intensity 
    2) fit position and line width
    3) fit all the parameters

    Args:
        x: Axis 
        data: data in an numpy array 
        dims: number of dimensions 
        lineShape: lineShape class 
        start: dictionary with the start parameters

    Returns:
        result2: This is the result object from lmfit from the final fitting step 
    '''
    
    start['intensity'] = np.max(data)/2.

    params = setup_params(dims, lineShape, start)
    kws  = {'options': {'maxiter':1000}}
    if lineShape.mixing == True:
        mixingState = True
    else:
        mixingState = False
    
    fit_args = ( x, data, dims, lineShape,start,mixingState)

    #print '===//=== Fit intensity and position ===//==='
    # adjust params for the fist fit:
    
    for i in params:
        params[i].set(vary=False)

    for tag in lineShape.fit_1:
        for entry in params:
            if tag in entry:
                params[entry].set(vary=True)

    minner = Minimizer(residual, params, fcn_args=fit_args,)
    result = minner.minimize()
    # write error report
    #print report_fit(result)

    #print '===//=== Fit position  ===//==='
    params_2 = result.params

    for i in params_2:
        params_2[i].set(vary=False)

    for tag in lineShape.fit_2:
        for entry in params:
            if tag in entry:
                params_2[entry].set(vary=True)
            
    params_2['intensity'].set(vary=False)
    minner = Minimizer(residual, params_2, fcn_args=fit_args,)
    result1 = minner.minimize()
    #print report_fit(result1)    

    #print '===//=== Fit all ===//==='
    params_3 = result1.params
    for i in params_3:
        params_3[i].set(vary=True)

    minner = Minimizer(residual, params_3, fcn_args=fit_args,)
    result2 = minner.minimize()
    #print report_fit(result2)    
    
    strings = []
    strings.append( '===//=== Fit Report ===//===')
    strings.append(  'Fit was successful: '+ str( result2.success))
    strings.append( 'chi square: %0.3f' %(result2.chisqr))
    strings.append('reduced chi square: %0.3f' %(result2.redchi))
    for i in result2.params:
        strings.append( '%10s %0.5f +/- %0.5f' % (i, result2.params[i].value,result2.params[i].stderr))
    strings.append('============================')


    fname = name+'.report'
    f = open(fname, 'w')
    strings = '\n'.join(strings)
    fileIo.printWrite(strings, f)
    f.close()

    return result2

    





