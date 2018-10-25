import numpy as np
import scipy
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
from . import lineShapes as ls
from . import fileIo
import decimal

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
        
        elif mixingState == 'theta_mixing':
            theta_tag = '%s_theta' %(peak)
            theta = params[theta_tag]   
            mixing = params['%s_mixing' % (peak)]
            model = lineShape.func(x, params[intensity_tag], shifts, lws, theta, mixing)
        
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
    #print np.sum(resid**2)
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
            shift_min = shift_val - lw_val
            shift_max = shift_val + lw_val



            params.add(lw_tag, vary=False, value=lw_val, min=0)
            params.add(shift_tag, vary=False, value=shift_val, min=shift_min, max=shift_max)
            params.add(intensity_tag, vary=False, value=start_int)

            if lineShape.mixing == True:
            	mixing_tag = '%s_mixing_%i'%(peak, i)
            	params.add(mixing_tag, vary=False, value=0.2, min=0, max=1)
            
        if lineShape.mixing == 'theta_mixing':
            mixing_tag = '%s_mixing'%(peak)
            params.add(mixing_tag, vary=False, value=0.2, min=0, max=1)


        if lineShape.mixing == 'theta' or lineShape.mixing == 'theta_mixing':
            theta_tag = '%s_theta' % (peak)
            params.add(theta_tag, vary=True, value=0,)

    return params

def change_params_varry(params, tags):

    for i in params:
        params[i].set(vary=False)

        for entry in tags:
            if entry in i:
                params[i].set(vary=True)
            if entry == 'intensity':
                params[i].set(value=params[i].value)

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

    change_params_varry(params, lineShape.fit_1)

    minner = Minimizer(residual, params, fcn_args=fit_args,)
    result = minner.minimize()
    print 'fit 1: complete'
    # write error report
    #print report_fit(result)

    #print '===//=== Fit position  ===//==='
    params_2 = change_params_varry(result.params, lineShape.fit_2)

    minner = Minimizer(residual, params_2, fcn_args=fit_args,)
    result2 = minner.minimize()
    print 'fit 2: complete'
    

    params_3 = change_params_varry(result2.params, lineShape.fit_3)

    minner = Minimizer(residual, params_3, fcn_args=fit_args,)
    result3 = minner.minimize()

    strings = []
    strings.append( '===//=== Fit Report ===//===')
    strings.append(  'Fit was successful: '+ str( result3.success))
    strings.append( 'chi square: %0.3f' %(result3.chisqr))
    strings.append('reduced chi square: %0.3f' %(result3.redchi))
    for i in result3.params:
        decimal_value = '%.3E' % decimal.Decimal(result3.params[i].value)
        decimal_err = '%.3E' % decimal.Decimal(result3.params[i].stderr)
        strings.append( '%20s %s +/- %s' % (i, decimal_value,decimal_err))
    strings.append('============================')
    
    for i in result3.params:
        print result3.params[i]

    name = '_'.join(group)
    fname = name+'.report'
    f = open(fname, 'w')
    strings = '\n'.join(strings)
    fileIo.printWrite(strings, f)
    f.close()

    return result2







