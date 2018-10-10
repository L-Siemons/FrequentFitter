import lineShapes as ls

class Gauss():
    """class for the Guassian line shape"""
    def __init__(self,):
        self.fit_1 = ['lw', 'intensity']
        self.fit_2 = ['lw', 'shift']
        self.fit_3 = ['lw', 'shift', 'intensity']
        self.func = ls.ndGaussian
        self.mixing = False

class Loren():
    """ ndLorentzian line shape"""
    def __init__(self,):
        self.fit_1 = ['lw', 'intensity']
        self.fit_2 = ['lw', 'shift']
        self.fit_3 = ['lw', 'shift', 'intensity']
        self.func = ls.ndLorentzian
        self.mixing = False

class Glore():
    """ ndLorentzian line shape"""
    def __init__(self,):
        self.fit_1 = ['lw', 'intensity', 'mixing']
        self.fit_2 = ['lw', 'shift','mixing']
        self.fit_3 = ['lw', 'shift', 'intensity', 'mixing']
        self.func = ls.ndGlore
        self.mixing = True

class RotGauss():
    """ ndLorentzian line shape"""
    def __init__(self,):
        self.fit_1 = ['lw', 'intensity', 'mixing']
        self.fit_2 = ['lw', 'shift','mixing']
        self.fit_3 = ['lw', 'shift', 'intensity', 'mixing']
        self.func = ls.rotatable_gauss_2D
        self.mixing = 'theta'
