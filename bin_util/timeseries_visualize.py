#%%
# -*- coding: utf-8 -*-
"""
Show the timeseries for a parcel.

TODO: Recently hasn't been tested anymore!!!
"""

import logging
import os
import sys
[sys.path.append(i) for i in ['.', '..']]

import numpy as np
import pandas as pd

import cropclassification.helpers.config_helper as conf
import cropclassification.helpers.pandas_helper as pdh

#-------------------------------------------------------------
# First define/init some general variables/constants
#-------------------------------------------------------------
# Get a logger...
logger = logging.getLogger(__name__)

# Constants for types of sensor data
SENSORDATA_VV = 'VV' # Vertical Vertical
SENSORDATA_VH = 'VH' # Vertical Horizontal

#-------------------------------------------------------------
# The real work
#-------------------------------------------------------------

def show(input_parcel_filepath: str,
         filter_id: str):

    # Load input data...
    df = pdh.read_file(input_parcel_filepath)

    # Just keep one parcel
    id_column = 'UID'
    df = df[df[id_column] == filter_id]

    # Remove all unnecessary columns
    '''
    for column in df:
        if(not column.startswith(SENSORDATA_VV + '_')
           and not column.startswith(SENSORDATA_VH + '_')
           and not column == conf.columns['id']):
            df = df.drop(columns=column)
    '''

    # Set index for transpose
    df.set_index(id_column, inplace=True)

    # Transpose columns to rows to create time series
    df = df.transpose()
    df.reset_index(inplace=True)

    '''    
    df.rename(columns={'index':'polarization_date'}, inplace=True)

    # Split the date and the polarization, the drop the original column
    df.insert(0, 'polarization', df['polarization_date'].str.split('_').str.get(0))
    #df['polarization'] = df['polarization_date'].str.split('_').str.get(0)
    df.insert(1, 'date', df['polarization_date'].str.split('_').str.get(1))
    #df['date'] = df['polarization_date'].str.split('_').str.get(1)
    df = df.drop(columns='polarization_date')

    logger.info(df)

    # Pivot to put VV and VH in seperate columns
    df = df.pivot(index='date', columns='polarization')
    #df.unstack(level=-1)
    #df.set_index('date', inplace=True)

    df = df[filter_id]
    df[SENSORDATA_VH + '/' + SENSORDATA_VV] = np.log10(df[SENSORDATA_VH] / df[SENSORDATA_VV])*10
    df[SENSORDATA_VH] = np.log10(df[SENSORDATA_VH])*10
    df[SENSORDATA_VV] = np.log10(df[SENSORDATA_VV])*10

    for column in df:
        logger.info(column)
    '''
    
    logger.info(df)

    # Plot
    df.plot()
    
# If the script is run directly...
if __name__ == "__main__":
        
    local_data_basedir = r"X:\Monitoring\Markers\playground\market"
    local_data_dir = os.path.join(local_data_basedir, r"output\baresoil")
    input_parcel_filepath = os.path.join(local_data_dir , "Lijst_percelen_Datum.csv") #moet sqllite zijn?
    show(input_parcel_filepath, filter_id = '0000280864DEAAE200000011')

