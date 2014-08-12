#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest
from math import *
import random as random
import time as time

def zdt1(individual):
    """ZDT1 multiobjective function.
    
    :math:`g(\\mathbf{x}) = 1 + \\frac{9}{n-1}\\sum_{i=2}^n x_i`
    
    :math:`f_{\\text{ZDT1}1}(\\mathbf{x}) = x_1`
    
    :math:`f_{\\text{ZDT1}2}(\\mathbf{x}) = g(\\mathbf{x})\\left[1 - \\sqrt{\\frac{x_1}{g(\\mathbf{x})}}\\right]`
    """
    g  = 1.0 + 9.0*sum(individual[1:])/(len(individual)-1)
    f1 = individual[0]
    f2 = g * (1 - sqrt(f1/g))
    return f1, f2

def zdt6(individual):
    """ZDT6 multiobjective function.
    
    :math:`g(\\mathbf{x}) = 1 + 9 \\left[ \\left(\\sum_{i=2}^n x_i\\right)/(n-1) \\right]^{0.25}`
    
    :math:`f_{\\text{ZDT6}1}(\\mathbf{x}) = 1 - \\exp(-4x_1)\\sin^6(6\\pi x_1)`
    
    :math:`f_{\\text{ZDT6}2}(\\mathbf{x}) = g(\\mathbf{x}) \left[ 1 - (f_{\\text{ZDT6}1}(\\mathbf{x})/g(\\mathbf{x}))^2 \\right]`
    
    """
    g  = 1 + 9 * (sum(individual[1:]) / (len(individual)-1))**0.25
    f1 = 1 - exp(-4*individual[0]) * sin(6*pi*individual[0])**6
    f2 = g * (1 - (f1/g)**2)
    return f1, f2

def uniform(low, up, size=None):
    try:
        return [random.uniform(a, b) for a, b in zip(low, up)]
    except TypeError:
        return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]


#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
# Unit testing
#===============================================================================

class DesignSpaceBasicTests(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(whoami())
        myLogger.setLevel("CRITICAL")
        print("Setup")
        myLogger.setLevel("DEBUG")

    def test010_SimpleCreation(self):
        #NDIM = 30
        n_evals = 1000000
        start_time = time.time()        
        for i in range(n_evals):
            this_ind = uniform(0,1,30)
            #print())
            res = zdt6(this_ind)
        elapsed_time = time.time() - start_time
        print('Total seconds {}'.format(elapsed_time))
        print('Milliseconds per eval {}'.format( elapsed_time/n_evals * 1000))
        
                       
            