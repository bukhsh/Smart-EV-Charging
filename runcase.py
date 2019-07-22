#==================================================================
# runcase.py
# This is a second level OATS script, which is called by the runfile.
# This script receives model,testcase, options as an input to run simulation
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# April 2018
# OATS
# Copyright (c) 2017 by W. Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3. (see LICENSE file for details).
#==================================================================

#===============Import===============
from __future__ import division
from selecttestcase import selecttestcase
from selectmodel import selectmodel
import os
from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition
from printdata import printdata
from printoutput import printoutput
import logging

#====================================

def runcase(testcase,mod,opt=None):
    print ('Selected model is: ', mod)
    print ('Selected testcase is: ', testcase)
    try:
        model = selectmodel(mod) #load model
        logging.info("Given model file found and selected from the models library")
    except Exception:
        logging.error("Given model file not found in the 'models' library", exc_info=False)
        raise
    try:
        ptc = selecttestcase(testcase) #read test case
        logging.info("Given testcase file found and selected from the testcase library")
    except Exception:
        logging.error("Given testcase  not found in the 'testcases' library", exc_info=False)
        raise
    datfile = 'datafile.dat'
    r = printdata(datfile,ptc,mod,opt)
    r.reducedata()
    r.printheader()
    r.printkeysets()
    r.printnetwork()
    r.printEV()


    ###############Solver settings####################
    if not opt['neos']:

        opt = SolverFactory(opt['solver'])
        #opt.options['mipgap'] = 0.1
        #################################################

        ############Solve###################
        instance = model.create_instance(datfile)
        instance.dual = Suffix(direction=Suffix.IMPORT)
        results = opt.solve(instance,tee=True)
        instance.solutions.load_from(results)
        # ##################################
        #
        #
        # ############Output###################
        o = printoutput(results, instance,mod)
        o.greet()
        o.solutionstatus()
        if 'UC' in mod:
            o.printUC()
        elif 'Storage' in mod:
            o.printStorage()
        else:
            o.printsummary()
            o.printoutputxls()

    else:
        instance = model.create_instance(datfile)
        solveroptions = SolverFactory(opt['solver'])
        solver_manager = SolverManagerFactory('neos')
        solver_manager.solve(instance, opt=solveroptions)
