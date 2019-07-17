#==================================================================
# select_testcase.py
# This Python script loads the test case file from the library
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3 (see LICENSE file for details).
#==================================================================

import pandas as pd

def selecttestcase(test):
    xl = pd.ExcelFile("testcases/"+test)

    df_bus             = xl.parse("bus")
    df_demand          = xl.parse("demand")
    df_branch          = xl.parse("branch")
    df_generators      = xl.parse("generator")
    df_shunt           = xl.parse("shunt")
    df_transformer     = xl.parse("transformer")
    df_EV              = xl.parse("EVs")
    df_EVsTravelDiary  = xl.parse("EVsTravelDiary")
    df_baseMVA         = xl.parse("baseMVA")
    df_ts              = xl.parse("timeseries")#,header=[0,1])

    data = {
    "bus": df_bus,
    "demand": df_demand,
    "branch": df_branch,
    "generator": df_generators,
    "shunt": df_shunt,
    "transformer": df_transformer,
    "EV":df_EV,
    "EVsTravelDiary":df_EVsTravelDiary,
    "baseMVA": df_baseMVA,
    "timeseries": df_ts
    }
    return data
