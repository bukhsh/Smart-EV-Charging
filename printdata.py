#==================================================================
# printdata.py
# A Python script to write data file for PYOMO
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3 (see LICENSE file for details).
#==================================================================
import datetime
import math
import sys
import pandas as pd
deltaT = 1.0
class printdata(object):
    def __init__(self,datfile,data,model,options):
        self.datfile     = datfile
        self.data        = data
        self.model       = model
        self.options     = options
    def reducedata(self):
        self.data["demand"]      = self.data["demand"].drop(self.data["demand"][self.data["demand"]['stat'] == 0].index.tolist())
        self.data["branch"]      = self.data["branch"].drop(self.data["branch"][self.data["branch"]['stat'] == 0].index.tolist())
        self.data["shunt"]       = self.data["shunt"].drop(self.data["shunt"][self.data["shunt"]['stat'] == 0].index.tolist())
        self.data["transformer"] = self.data["transformer"].drop(self.data["transformer"][self.data["transformer"]['stat'] == 0].index.tolist())
        self.data["generator"]   = self.data["generator"].drop(self.data["generator"][self.data["generator"]['stat'] == 0].index.tolist())
        self.data["EV"]          = self.data["EV"].drop(self.data["EV"][self.data["EV"]['stat'] == 0].index.tolist())
    def printheader(self):
        f = open(self.datfile, 'w')
        #####PRINT HEADER--START
        f.write('#This is Python generated data file for Pyomo model DCLF.py\n')
        f.write('#_author_:W. Bukhsh\n')
        f.write('#Time stamp: '+ str(datetime.datetime.now())+'\n')
        f.close()
    def printkeysets(self):
        f = open(self.datfile, 'a')
        ##===sets===
        #---set of buses---
        f.write('set B:=\n')
        for i in self.data["bus"].index.tolist():
            f.write(str(self.data["bus"]["name"][i])+"\n")
        f.write(';\n')
        #---set of generators---
        f.write('set G:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+"\n")
        f.write(';\n')
        #---set of demands---
        f.write('set D:=\n')
        for i in self.data["demand"]["name"].unique():
            f.write(str(i)+"\n")
        f.write(';\n')
        ###---set of EVs---
        if len(self.data["EV"]["name"])!=0:
            f.write('set EV:=\n')
            for i in self.data["EV"]["name"].unique():
                f.write(str(i)+"\n")
            f.write(';\n')

            f.write('set EVWindow:=\n')
            for i in self.data["EV"]["name"].unique():
                for window in range(1,7):
                    f.write(str(i)+" "+str(window)+"\n")
            f.write(';\n')

        #---EVs-bus mapping---
        if len(self.data["EV"]["name"])!=0:
            f.write('set EVbs:=\n')
            for i in self.data["EV"].index.tolist():
                f.write(str(self.data["EV"]["busname"][i]) + " "+str(self.data["EV"]["name"][i])+"\n")
            f.write(';\n')
            #---EV flexibility windows---
            df_flex = pd.DataFrame(columns={'EV','Window','Start','End','SoCStart','SoCEnd'})
            ind = 0
            f.write('set EVFlexWindow:= \n')
            for i in self.data["EV"].index.tolist():
                window = 1
                lst = self.data["EVsTravelDiary"]["name"][self.data["EV"]['name'][i]==self.data["EVsTravelDiary"]["name"]].index.tolist()
                for ev in lst:
                    f.write(str(str(self.data["EVsTravelDiary"]['name'][ev])+" "+str(window)+" "+str(1)+"\n"))
                    f.write(str(str(self.data["EVsTravelDiary"]['name'][ev])+" "+str(window)+" "+str(2)+"\n"))
                    df_flex.loc[ind] = pd.Series({'EV':self.data["EVsTravelDiary"]['name'][ev],'Window':window,\
                    'Start':self.data["EVsTravelDiary"]['t_in'][ev],'End':self.data["EVsTravelDiary"]['t_out'][ev],\
                    'SoCStart':self.data["EVsTravelDiary"]['EStart'][ev],'SoCEnd':self.data["EVsTravelDiary"]['EEnd'][ev]})

                    ind += 1
                    window += 1
            f.write(';\n')

            f.write('set FlexTimes:= \n')
            for i in df_flex.index.tolist():
                for t in range(int(df_flex["Start"][i]),int(df_flex["End"][i])+1):
                    f.write(str(int(df_flex["EV"][i]))+" "+str(int(df_flex["Window"][i]))+" "+str(t)+"\n")
            f.write(';\n')

            f.write('set FlexTimesRed:= \n')
            for i in df_flex.index.tolist():
                for t in range(int(df_flex["Start"][i])+1,int(df_flex["End"][i])+1):
                    f.write(str(int(df_flex["EV"][i]))+" "+str(int(df_flex["Window"][i]))+" "+str(t)+"\n")
            f.write(';\n')
            # flexibility times


            f.write('set EVBoundaryStart:= \n')
            for i in df_flex.index.tolist():
                f.write(str(int(df_flex["EV"][i]))+" "+str(int(df_flex["Window"][i]))+" "+str(int(df_flex["Start"][i]))+"\n")
            f.write(';\n')
            f.write('set EVBoundaryEnd:= \n')
            for i in df_flex.index.tolist():
                f.write(str(int(df_flex["EV"][i]))+" "+str(int(df_flex["Window"][i]))+" "+str(int(df_flex["End"][i]))+"\n")
            f.write(';\n')


            f.write('param SoCStart:= \n')
            for i in df_flex.index.tolist():
                f.write(str(int(df_flex["EV"][i]))+" "+str(int(df_flex["Window"][i]))+" "+str(int(df_flex["Start"][i]))+" "+str(round(df_flex["SoCStart"][i],2))+"\n")
            f.write(';\n')
            f.write('param SoCEnd:= \n')
            for i in df_flex.index.tolist():
                f.write(str(int(df_flex["EV"][i]))+" "+str(int(df_flex["Window"][i]))+" "+str(int(df_flex["End"][i]))+" "+str(round(df_flex["SoCEnd"][i],2))+"\n")
            f.write(';\n')

        #---set of time-periods---
        f.write('set T:= \n')
        for i in self.data["timeseries"]['timeperiod']:
            f.write(str(i) + "\n")
        f.write(';\n')
        f.write('set TRed:= \n')
        for i in self.data["timeseries"]['timeperiod'][1:-1]:
            f.write(str(i) + "\n")
        f.write(';\n')
        f.close()

    def printnetwork(self):
        f = open(self.datfile, 'a')
        f.write('set LE:=\n 1 \n 2;\n')
        f = open(self.datfile, 'a')
        f.write('set Window:=\n 1 \n 2\n 3\n 4\n 5\n 6;\n')
        #set of transmission lines
        f.write('set L:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+"\n")
        f.write(';\n')
        #set of transformers
        if len(self.data["transformer"]["name"])!=0:
            f.write('set TRANSF:= \n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+"\n")
            f.write(';\n')
        #---set of generator-bus mapping (gen_bus, gen_ind)---
        f.write('set Gbs:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["busname"][i]) + " "+str(self.data["generator"]["name"][i])+"\n")
        f.write(';\n')
        #---set of demand-bus mapping (demand_bus, demand_ind)---
        f.write('set Dbs:=\n')
        for i in self.data["demand"].index.tolist():
            f.write(str(self.data["demand"]["busname"][i]) + " "+str(self.data["demand"]["name"][i])+"\n")
        f.write(';\n')
        #---set of reference bus---
        f.write('set b0:=\n')
        slackbus = self.data["generator"]["busname"][self.data["generator"]["type"]==3].tolist()
        for i in slackbus:
            f.write(str(i)+""+"\n")
        f.write(';\n')
        #---param defining system topolgy---
        f.write('param A:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+"1"+" "+str(self.data["branch"]["from_busname"][i])+"\n")
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+"2"+" "+str(self.data["branch"]["to_busname"][i])+"\n")
        f.write(';\n')
        #---Transformers---
        if len(self.data["transformer"]["name"])!=0:
            f.write('param AT:= \n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+"1"+" "+str(self.data["transformer"]["from_busname"][i])+"\n")
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+"2"+" "+str(self.data["transformer"]["to_busname"][i])+"\n")
            f.write(';\n')
        f.close()
    def printEV(self):
        f = open(self.datfile, 'a')
        #---Tranmission line chracteristics for DC load flow---
        f.write('param BL:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(-1/float(self.data["branch"]["x"][i]))+"\n")
        f.write(';\n')
        #---Transformer chracteristics---
        if len(self.data["transformer"]["name"])!=0:
            f.write('param BLT:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(-float(1/self.data["transformer"]["x"][i]))+"\n")
            f.write(';\n')
        #---Tranmission line bounds---
        f.write('param SLmax:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(float(self.data["branch"]["ContinuousRating"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        #---Transformer chracteristics---
        if len(self.data["transformer"]["name"])!=0:
            f.write('param SLmaxT:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(float(self.data["transformer"]["ContinuousRating"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')


        #===parameters===
        #---Real power demand---
        f.write('param PD:=\n')
        for i in self.data["timeseries"]:
            if 'time' not in i:
                for j in self.data["timeseries"][i].index.tolist():
                    f.write(str(i)+" "+str(self.data["timeseries"]["timeperiod"][j])+" "+str(float(self.data["timeseries"][i][j])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param VOLL:=\n')
        for i in self.data["demand"].index.tolist():
            f.write(str(self.data["demand"]["name"][i])+" "+str(float(self.data["demand"]["VOLL"][i]))+"\n")
        f.write(';\n')
        f.write('param baseMVA:=\n')
        f.write(str(self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')

        #---Real power generation bounds---
        f.write('param PGmin:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["PGLB"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param PGmax:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["PGUB"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        #---ramp rates---
        f.write('param RampUp:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(deltaT*self.data["generator"]["RampUp(MW/hr)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param RampDown:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(deltaT*self.data["generator"]["RampDown(MW/hr)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')

#        #---cost data---
#        f.write('param cost:=\n')
#        for i in self.data["cost"].index.tolist():
#            f.write(str(self.data["cost"]["name"][i])+" "+str(self.data["cost"]["timeperiod"][i])+" "+str(self.data["cost"]["cost(pounds/kwh)"][i])+"\n")
#        f.write(';\n')
#        
        #---V2G: System Buy Price (SBP -- charging) and System Sell Price (SSP -- discharging)        
        f.write('param SBP:=\n')
        for i in self.data["cost"].index.tolist():
            f.write(str(self.data["cost"]["name"][i])+" "+str(self.data["cost"]["timeperiod"][i])+" "+str(self.data["cost"]["SBP(pounds/kwh)"][i])+"\n")
        f.write(';\n')
        
        f.write('param SSP:=\n')
        for i in self.data["cost"].index.tolist():
            f.write(str(self.data["cost"]["name"][i])+" "+str(self.data["cost"]["timeperiod"][i])+" "+str(self.data["cost"]["SSP(pounds/kwh)"][i])+"\n")
        f.write(';\n')

        if len(self.data["EV"]["name"])!=0:
            f.write('param ChargeEff:=\n')
            for i in  self.data["EV"].index.tolist():
                f.write(str(self.data["EV"]["name"][i])+" "+str(float(self.data["EV"]["ChargingEfficiency(%)"][i])/100.0)+"\n")
            f.write(';\n')
            f.write('param PVUB:=\n')
            for i in  self.data["EV"].index.tolist():
                f.write(str(self.data["EV"]["name"][i])+" "+str(float(self.data["EV"]["capacity(kW)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
            f.write('param EVUB:=\n')
            for i in  self.data["EV"].index.tolist():
                f.write(str(self.data["EV"]["name"][i])+" "+str(float(self.data["EV"]["battery(kWh)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')

        f.close()
