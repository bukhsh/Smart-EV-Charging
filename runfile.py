#==================================================================
# runfile.py
# This is a top level script.
# EV charging scheduling problem
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2019 by W. Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3. (see LICENSE file for details).
#==================================================================

from runcase import runcase
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='oatslog.log',
                    filemode='w')
logging.info("EV Scheduling log file")

#----------------------------------------------------------------------
def main():
    logging.info("Program started")
    #options
    opt=({'neos':False,\
    'solver':'cplex'})


    # =====Test cases=====
    #give a path to the testcase file under the 'testcase' folder
    testcase = 'SP53224_10020195.xlsx'
    # testcase = 'case24_ieee_rts.xlsx'
    #testcase = 'case2.xlsx'
    # =====Model=====
    #specify a model to solve
    model ='EVSchedule'
    # ==log==
    logging.info("Solver selected: "+opt['solver'])
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,opt)
    logging.info("Done!")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.error("Fatal error in main loop", exc_info=True)
        raise
