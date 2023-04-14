'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np

def read_data():
    my_df = pd.read_csv('../MergeData.csv',sep=';',encoding="cp1252")
    my_df = my_df.replace(314004824, 'Locataire: Montréal')
    my_df = my_df.replace(315107746, 'Propriétaire: Laval')
    return my_df

def filter(df):
    df = df.drop(columns=['Code de consommation', 'Code de température'])
    df['Date et heure'] = pd.to_datetime(df['Date et heure'])
    return df

def get_separate_data(df):
    tenant_df = df[df['Contrat'] != 'Propriétaire: Laval']
    homeowner_df = df[df['Contrat'] == 'Propriétaire: Laval']
    return tenant_df, homeowner_df

def avg_consumption_per_temp(tenant_df, homeowner_df):
    tenant_df_avg = tenant_df.groupby(tenant_df['Température moyenne (°C)'], as_index=False)['kWh'].mean()
    homeowner_df_avg = homeowner_df.groupby(homeowner_df['Température moyenne (°C)'], as_index=False)['kWh'].mean()
    return tenant_df_avg, homeowner_df_avg

def group_by_season(df):
    #source for seasons: https://nrc.canada.ca/en/certifications-evaluations-standards/canadas-official-time/3-when-do-seasons-start
    df = df.sort_values(['Date et heure'])

    df['Saison'] = ""
    df['Saison'] = np.where((df['Date et heure'] >= '2022-06-01') & (df['Date et heure'] <= '2022-06-20'), 'Printemps', df['Saison'])
    df['Saison'] = np.where((df['Date et heure'] >= '2022-06-21') & (df['Date et heure'] <= '2022-09-22'), 'Été', df['Saison'])
    df['Saison'] = np.where((df['Date et heure'] >= '2022-09-23') & (df['Date et heure'] <= '2022-12-21'), 'Automne', df['Saison'])
    df['Saison'] = np.where((df['Date et heure'] >= '2022-12-22') & (df['Date et heure'] <= '2023-03-20'), 'Hiver', df['Saison'])
    df['Saison'] = np.where((df['Date et heure'] >= '2023-03-21') & (df['Date et heure'] <= '2023-06-21'), 'Été', df['Saison'])
    df = df[df['Saison'] != '']
    avg_data_df = df.groupby(df['Saison'], as_index=False)['kWh', 'Température moyenne (°C)'].mean()
    return avg_data_df
   

    

       
