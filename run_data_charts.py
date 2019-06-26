# #_author_Waqquas Bukhsh
# #A glomy Friday evening in Glasgow, sitting on my desk and try to proces this data for a shitty journal paper that I am planning to write. While I write this code I am wondering what the fuck am I doing with my life. I should be out changing the world for better, putting my energy to good use, but man o man the reluctance to take risk, and to be fare, pay mortage and make both ends meet demands that I sit in this chair, write (or try to write) this damn article that no body is probably going to read in 10 years and no difference it is going to make to the world. well enough bittering, lets get on with this shit work
#
import pandas as pd
import datetime as dt
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib2tikz import save as tikz_save

#
# #
# # df_wind   = pd.read_csv('data/wind/scen_zone1.out')
# # df_wind   = pd.read_csv('data/wind/scen_zone5.out')
# # df_wind   = pd.read_csv('data/wind/scen_zone9.out')
# # df_wind   = pd.read_csv('data/wind/scen_zone12.out')
# df_wind   = pd.read_csv('data/wind/scen_zone13.out')
# # df_wind=df_wind.drop(df_wind.index[[48]])
#
# del df_wind['Unnamed: 0']
#
# for key in df_wind:
#     df_wind[key].plot()
# tikz_save("wind_zone13.tex")
# plt.show()











##====Demand====
df_demand = pd.read_csv('data/demand.csv')

df_demand_mod = pd.DataFrame(columns={'demand'})
df_demand.index = df_demand[' timestamp']
df_demand.index = pd.to_datetime(df_demand.index)
del df_demand[' timestamp']


#
#
hourly_summary = pd.DataFrame()
#normalise and scale with peak demand in the ieee 24 bus case
df_demand[' demand'] = 2850*df_demand[' demand']/df_demand[' demand'].max()

hourly_summary['demand'] = df_demand[' demand'].resample('30min').mean()

demand_date = '2018-02-01'


# hour = pd.to_timedelta(hourly_summary.index.hour)
# day_average =  hourly_summary.groupby([hourly_summary.index.hour,hourly_summary.index.minute]).mean()
# day_std =  hourly_summary.groupby([hourly_summary.index.hour,hourly_summary.index.minute]).std()
#
# df_halfhourly = pd.DataFrame(columns={'mean','std'})
#
# df_halfhourly['mean'] = day_average['demand']
# df_halfhourly['std'] = day_std['demand']
#
# df_halfhourly.to_csv('halfhourly_demand_scaled24bus_averages.csv',index=False)
#
# # ax = day_average.plot()
# # (day_average+day_std).plot(ax=ax)
# # (day_average-day_std).plot(ax=ax)
# # plt.show()
