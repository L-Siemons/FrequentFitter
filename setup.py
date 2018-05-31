from distutils.core import setup
from setuptools import setup, find_packages

descrip='''

FrequentFitter is a program for fitting 
NMR peaks that was heavily inspired by Fuda

written by Lucas Siemons

'''

setup(
    name='frequentFitter',
    version='1.0',
    author='L. Siemons',
    author_email='lucas.siemons@googlemail.com',
    packages=find_packages(),
    #scripts=[''],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description=descrip,
    long_description=open('README.txt').read(),
    install_requires=['numpy','nmrglue','scipy', 'lmfit',],    
)
