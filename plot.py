# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:20:26 2020

@author: james
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

V2gstring = input('Routine/minimal?')

if 'm' in V2gstring.lower():
    tit = 'Minimal'
else:
    tit = 'Routine'

#tit+= ' Oneway'
tit+= ' V2G'

sns.set_style('whitegrid')

res = pd.read_excel('results\\results.xlsx', sheet_name = 'summary')

testcase = 'v2g_test_minimal_flatcost.xlsx'
prices = pd.read_excel('testcases\\'+testcase, sheet_name= 'timeseriesGen')

EVs = pd.read_excel('testcases\\'+testcase, sheet_name= 'EVs').name.unique().tolist()

EVres = pd.read_excel('results\\results.xlsx', sheet_name = 'EVs')

fig,ax = plt.subplots(figsize=(10,8))
ax2 = ax.twinx()


ax.plot(res['Time period'], res['Conventional generation (kW)'], label='Generation',color = sns.color_palette()[0])
ax.plot(res['Time period'], res['Demand (kW)'], label='Domestic demand',color = sns.color_palette()[1])

#plot individual EVs - first five
#EVcnt=4
#for EV in EVs[0:5]:
#    ax.plot(EVres[EVres.name == EV]['Time period'], EVres[EVres.name == EV]['Charging(kW)']-EVres[EVres.name == EV]['Discharging(kW)'],label=str(EV),color=sns.color_palette()[EVcnt])
#    EVcnt+=1
    
#plot all EVs together
charging_profile=[]
discharging_profile=[]
net_profile=[]
for t in range(144):
    
    charging_profile.append(EVres[EVres['Time period'] == t]['Charging(kW)'].sum())
    discharging_profile.append(EVres[EVres['Time period'] == t]['Discharging(kW)'].sum())
    net_profile.append(EVres[EVres['Time period'] == t]['Charging(kW)'].sum()-EVres[EVres['Time period'] == t]['Discharging(kW)'].sum())

ax.plot(res['Time period'], charging_profile, label='EV charging (sum)',color=sns.color_palette()[4])
ax.plot(res['Time period'], discharging_profile, label='EV discharging (sum)',color=sns.color_palette()[5])
ax.plot(res['Time period'], net_profile, label='Net EV power (sum)',color=sns.color_palette()[6])    


ax2.plot(res['Time period'], prices['SBP(pounds/kwh)'][0:144], label='SBP',color = sns.color_palette()[2])
ax2.plot(res['Time period'], prices['SSP(pounds/kwh)'][0:144], label='SSP',color = sns.color_palette()[3])

ax.set_xlabel('Time period',fontsize=16)
ax.set_ylabel('kW',fontsize=16)
ax2.set_ylabel('Cost',fontsize=16)

for t in ax.xaxis.get_majorticklabels(): t.set_fontsize(14)
for t in ax.yaxis.get_majorticklabels(): t.set_fontsize(14)
for t in ax2.yaxis.get_majorticklabels(): t.set_fontsize(14)

ax.legend(fontsize=14, loc='upper left')
ax2.legend(fontsize=14,loc='lower right')
plt.title(tit,fontsize=16)