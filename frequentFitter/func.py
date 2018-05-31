import nmrglue as ng

'''
This modules contains misc functions that so far have no 
clear grouping or don't seem worth giving their own sub package
'''

def get_index(val, axis, radius):
    '''
    Takes the index for the values in the axis at the
    that are closest to the boundary defined by the radius

    Args:
        val: peak position
        axis: dictionary containing the axis 
        radius: the radius

    Returns:
        tuple: contains the indicies  at each extreme of the radius
    '''
    check = True
    min_ = None


    for i,j in enumerate(axis):

        if j <= val + radius:
            if min_ == None:
                min_ = i
        
        if j <= val - radius:
            max_ = i
            break

    #print min_, max_
    return (min_,max_)

def collect_axis(dims, dic, data):
    '''
    Collects the NMR glue axis into a dictionary

    Args:
        dims: number of dimensions 
        dic: dictionary returned by ng.pipe.read
        data: data returned by ng.pipe.read

    Returns: 
        axis: dictionary containing the axis
    '''

    axis = {}
    for i in range(dims):
        uc = ng.pipe.make_uc(dic, data, dim=i)
        ppm_axis = uc.ppm_scale()
        #ppm_13c_0, ppm_13c_1 = uc_13c.ppm_limits()

        axis[i] = ppm_axis
        print 'dim', i, len(ppm_axis)
    return axis

def ndm(*args):
    '''
    A magic function found here 
    https://stackoverflow.com/questions/22774726/numpy-evaluate-function-on-a-grid-of-points
    '''

    return [x[(None,)*i+(slice(None),)+(None,)*(len(args)-i-1)] for i, x in enumerate(args)]

def elipsoid(pos,peak):
    '''
    This evaluates if a point is inside the ellipsoid.
    '''
    
    working = 0.
    for dim in peak:
        print dim

