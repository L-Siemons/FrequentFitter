from . import lineShapes as ls

class Basic_lineShape():
    """class for the Guassian line shape"""
    def __init__(self,):
        self.fit_1 = ['lw', 'intensity']
        self.fit_2 = ['lw', 'shift']
        self.fit_3 = ['lw', 'shift', 'intensity']


class Gauss():
    """class for the Guassian line shape"""
    def __init__(self,):
        self.fit_1 = ['intensity','lw']
        self.fit_2 = ['lw', 'shift']
        self.fit_3 = ['lw', 'shift', 'intensity']
        self.func = ls.ndGaussian
        self.mixing = False

class Loren():
    """ ndLorentzian line shape"""
    def __init__(self,):
        self.fit_1 = ['intensity','lw']
        self.fit_2 = ['lw', 'shift']
        self.fit_3 = ['lw', 'shift', 'intensity']
        self.func = ls.ndLorentzian
        self.mixing = False

class Glore():
    """ ndLorentzian line shape"""
    def __init__(self,):
        self.fit_1 = ['intensity','lw']
        self.fit_2 = ['lw', 'shift','mixing']
        self.fit_3 = ['lw', 'shift', 'intensity', 'mixing']
        self.func = ls.ndGlore
        self.mixing = True

class RotGauss():
    """ ndLorentzian line shape"""
    def __init__(self,):
        self.fit_1 = ['intensity','lw']
        self.fit_2 = ['lw', 'shift', 'theta']
        self.fit_3 = ['lw', 'shift', 'intensity',]
        self.func = ls.rotatable_gauss_2D
        self.mixing = 'theta'

class Rotlorren():
    """ ndLorentzian line shape"""
    def __init__(self,):
        self.fit_1 = ['intensity','lw']
        self.fit_2 = ['lw', 'shift', 'theta']
        self.fit_3 = ['lw', 'shift', 'intensity', 'theta']
        self.func = ls.rotatable_lorren_2D
        self.mixing = 'theta'

class Rotglore():
    """ ndLorentzian line shape"""
    def __init__(self,):
        self.fit_1 = ['intensity','lw']
        self.fit_2 = ['lw', 'shift', 'theta','mixing']
        self.fit_3 = ['lw', 'shift', 'intensity','mixing', 'theta']
        self.func = ls.rotatable_glore_2D
        self.mixing = 'theta_mixing'

class RotXglore():
    """ ndLorentzian line shape"""
    def __init__(self,):
        self.fit_1 = ['intensity','lw']
        self.fit_2 = ['lw', 'shift', 'theta','mixing']
        self.fit_3 = ['lw', 'shift', 'intensity', 'mixing' , 'theta']
        self.func = ls.rotatable_x_glore_2D
        self.mixing = 'theta_mixing'
