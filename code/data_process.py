import pandas as pd
from sodapy import Socrata
from matplotlib import pyplot as plt
import os
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.structure import SoftmaxLayer
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
import numpy as np
from joblib import Parallel, delayed
import  multiprocessing
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier





def integral(data):
    if data == -1:
        return -1
    else:
        if (ord(data) - 48) > 16:
            return ord(data) - 55
        else:
            return ord(data) - 48

def modify_data(data):
    x = 0

def grade_level(row):
    df_need = results_df[results_df[u'Year'] == row[u'Year']]
    df_need = df_need[df_need[u'Job Class'] == row[u'Job Class']]
    row[u'Grade Level'] = df_need[row[u'Pay Grade'] <= df_need[u'Pay Grade']].count() / df_need[u'Pay Grade'].count()
    print row[u'Grade Level']
    return row

def tmp_func(df):
 df = df.apply(modify_data,axis = 1)
 return df

def apply_parallel(df_grouped, func):
 results = Parallel(n_jobs=-1)(delayed(func)(group) for name, group in df_grouped)
 return pd.concat(results)

if __name__ == '__main__':

    #read raw data
    results_df = pd.read_csv(u'City_Employee_Payroll.csv')

    # pay grade fillna

    # pay grade adjustment
    # pay grade standarize
    results_df[u'Pay Grade'] = results_df[u'Pay Grade'].fillna(-1)
    results_df[u'Pay Grade'] = results_df[u'Pay Grade'].apply(integral)
    #results_df.apply(grade_level,axis=1)

    #payroll department adjustment
    results_df[u'Payroll Department'] = results_df[u'Payroll Department'].fillna(69)
    #dummy_variable
    results_df = pd.get_dummies(results_df, prefix=u'Department :',columns=[u'Payroll Department'])

    #employment type adjustment
    #dummy variable
    results_df = pd.get_dummies(results_df, prefix=u'Employment Type', columns=[u'Employment Type'])

    #job class adjustment
    l = len(results_df[u'Job Class'])
    #dummy variable
    results_df = pd.get_dummies(results_df, prefix=u'Job Class',columns=[u'Job Class'])





    results_df.to_csv(u'modified_train_data.csv')

