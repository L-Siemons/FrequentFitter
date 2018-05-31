'''
This is a modules for reading in files 
'''

import lineShapeClasses as lsc
import sys

def readInputFile(file):

    '''
    Reads in the input file 

    Args:
        file: The name of the input file

    Returns:
        peaks: Dictionary containing the parameters in the 
               input file 
        spectrum_name: The name of the NMR spectrum
    '''
    
    lineshape = None
    peaks = {}
    f = open(file,'r')
    for i in f.readlines():
        if i[0]!= '#':
            token = i.split('|')
            name = token[0].rstrip()
            if name == 'default':
                default_lw = [float(a) for a in token[2].split()]
                default_radius = [float(a) for a in token[3].split()]
                print 'Default radii:', default_radius
                print 'Default line widths', default_lw
            elif name == 'dataFile':
                spectrum_name = token[1].rstrip().strip()
            elif name == 'noise':
                noise = float(token[1].rstrip().strip())
            elif name == 'lineshape':
                lineshape = token[1].rstrip().strip()
            elif name == 'engine':
                engine = token[1].rstrip().strip()
            else:    
                peaks[name] = {}
                peaks[name]['position'] = [float(a) for a in token[1].split()]
                if len(token) < 3:
                    peaks[name]['lw'] = default_lw
                    peaks[name]['radius'] = default_radius
                else:
                    peaks[name]['lw'] = [float(a) for a in token[2].split()]
                    peaks[name]['radius'] = [float(a) for a in token[3].split()]

    for i in peaks:
        peaks[i]['noise'] = noise

    if lineshape == 'Gauss':
        lineshape = lsc.Gauss()
    elif lineshape == 'Glore':
        lineshape = lsc.Glore()
    elif lineshape == 'Loren':
        lineshape = lsc.Loren()
    else:
        print 'Line Shape doesnt exist (or is misspelt!)'
        sys.exit()
    print 'Read in:'
    print '--------'
    print 'spectrum name: ', spectrum_name
    for name in peaks:
        print '==//== ' +name+ ' ==//== '
        for i in peaks[name]:
            print i, peaks[name][i]

    f.close()
    return peaks, spectrum_name, lineshape

def gnuplotCommand(counter, peak,dataFile):
    
    gnuCommand =  ("splot '%s' i %i u 1:2:3 t 'Experimental' w linesp," %(dataFile,counter),
                   " '%s' i %i u 1:2:4 w lines t 'Group: %s'\n" %(dataFile,counter,peak),
                   "pause -1 'Press [ENTER] key to continue' \n")
    
    gnuCommandJoined = ''.join(gnuCommand)
    
    return gnuCommandJoined, counter+1

def printWrite(str, file):
    '''
    Prints to the screen and also writes to a file
    Args:
        str: string to use
        file: file to write in
    '''

    print str
    file.write(str)