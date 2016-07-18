# -*- coding: utf-8 -*-
"""

@author: ahmadpain
"""
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

loan = pd.read_csv('C:/Users/ahmadpain/Downloads/LoanStats3d.csv/LoanStats3d.csv',skiprows=1,parse_dates=True,index_col='id')
loan=loan.drop(['member_id', 'grade', 'sub_grade', 'emp_title', 'issue_d', 'pymnt_plan', 'url', 'desc', 'title', 'initial_list_status', 'last_pymnt_d', 'last_pymnt_amnt', 'next_pymnt_d', 'last_credit_pull_d', 'policy_code', 'addr_state','zip_code'], axis=1) 
loanbk = loan
'''Remove % symbol from the interest rate & revolving utilization '''
loan.int_rate=loan.int_rate.str.split('%',1).str[0] 
loan.revol_util=loan.revol_util.str.split('%',1).str[0]
'''Remove "months" from the loan period '''
loan.term=loan.term.str.split(' ',2).str[1]
num_del_90 = loan.loc[:,'num_tl_90g_dpd_24m']
num_del_90 = num_del_90.dropna()
num_del_90 = num_del_90.values
num_sats = loan.loc[:,'num_sats']
num_sats=num_sats.dropna()
num_sats = num_sats.values
N = len(num_sats)
area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
plt.scatter(num_sats,num_del_90,s=area,alpha=0.5)
plt.title("Scatter plot")
plt.xlabel("Number of satisfactory accounts")
plt.ylabel("Number of accounts 90 or more days past due in last 24 months")
plt.savefig('plot1.png',bbox_inches='tight')

N = 50
area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
emp_length=loan.loc[:,'emp_length']
emp_length=emp_length.str.split('+',1).str[0]
emp_length=emp_length.str.split('<',1).str[0]
emp_length=emp_length.str.split('years',1).str[0]
emp_length=emp_length.str.split('year',1).str[0]
emp_length=emp_length.str.split('n/a',1).str[0]
xx = emp_length.values
xx = xx[0:421095]
xx = xx.tolist()
xx = list(filter(lambda x: len(x)>0,xx));
xx = np.asarray(xx)
xx = xx.astype(int)
yy = num_sats.tolist()
while '' in xx:
    index = xx.index('')
    xx.remove('')
    yy[index] = np.nan
    
yy = yy[~np.isnan(yy)]
yy = np.asarray(yy)
yy = yy.astype(int)
area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
plt.title("Scatter plot")
plt.scatter(xx,yy[0:362938],s=area,alpha=0.5)
plt.ylabel("Number of satisfactory accounts")
plt.xlabel("employment length in number of years")
plt.savefig('plot2.png',bbox_inches='tight')