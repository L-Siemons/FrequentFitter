import numpy as np
import scipy
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
from . import lineShapes as ls
from . import fileIo


def plane(params, x, data, dims,lineShape,group, peaks):
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

    mixingState = lineShape.mixing
    planes = []

    for peak in group:
        shifts = [params['%s_shift_%i' % (peak, dim)] for dim in range(dims)]
        lws = [params['%s_lw_%i' % (peak, dim)] for dim in range(dims)]

        intensity_tag = '%s_intensity' % (peak)

        if mixingState == False:
            model = lineShape.func(x, params[intensity_tag], shifts, lws)

        elif mixingState == 'theta':
            theta_tag = '%s_theta' %(peak)
            theta = params[theta_tag]
            model = lineShape.func(x, params[intensity_tag], shifts, lws, theta)

        else:

    	    mixing = [params['%s_mixing_%i' % (peak, dim)] for dim in range(dims)]
            model = lineShape.func(x, params[intensity_tag], shifts, lws, mixing)

        planes.append(model)

    final_model = sum(planes)
    return final_model

def residual(params, x, data, dims,lineShape,group, peaks):
    final_model = plane(params, x, data, dims,lineShape,group, peaks)
    noise = float(peaks[peaks.keys()[0]]['noise'])
    resid = (data - final_model)/noise
    return resid

def setup_params(dims, lineShape, group, peaks, start_int):
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

    for peak in group:
        for i in range(dims):

            lw_tag = '%s_lw_%i' % (peak,i)
            shift_tag = '%s_shift_%i' % (peak,i)
            intensity_tag = '%s_intensity' % (peak)

            lw_val = peaks[peak]['lw'][i]
            shift_val = peaks[peak]['position'][i]

            params.add(lw_tag, vary=False, value=lw_val, min=0)
            params.add(shift_tag, vary=False, value=shift_val)
            params.add(intensity_tag, vary=False, value=start_int)

            if lineShape.mixing == True:
            	mixing_tag = '%s_mixing_%i'%(peak, i)
            	params.add(mixing_tag, vary=False, value=0.2, min=0, max=1)

        if lineShape.mixing == 'theta':
            theta_tag = '%s_theta' % (peak)
            params.add(theta_tag, vary=True, value=0)

    return params

def fit(x, data, dims, lineShape, group, peaks):

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

    start_int = np.max(data)/2.
    params = setup_params(dims, lineShape, group, peaks, start_int)
    kws  = {'options': {'maxiter':1000}}

    fit_args = ( x, data, dims,lineShape,group, peaks)

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

    for i in params_2.keys():
    	if 'intensity' in i:
            params_2[i].set(vary=False)
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

    name = '_'.join(group)
    fname = name+'.report'
    f = open(fname, 'w')
    strings = '\n'.join(strings)
    fileIo.printWrite(strings, f)
    f.close()

    return result2







