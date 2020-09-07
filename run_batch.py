#Author Calum Edmunds
#To run time series

from runfile import main
from shutil import copyfile

cases = ['','_N2EXcostcurve','_flatcostcurve']

for k in range(len(cases)):
    
    #Run optimisation for batch
    try:
        main('new/SP53224_new_SeparateSheet_with_infeasible_diaries'+str(cases[k])+'.xlsx')

        copyfile('results/results.xlsx', 'results/results'+str(cases[k])+'.xlsx')
    
    except:
        print('Fail on'+str(k))
              