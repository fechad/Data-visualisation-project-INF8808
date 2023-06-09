'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np

DAYS = {
    'Sunday': 'Dimanche',
    'Monday': 'Lundi',
    'Tuesday': 'Mardi',
    'Wednesday': 'Mercredi',
    'Thursday' : 'Jeudi',
    'Friday' : 'Vendredi',
    'Saturday': 'Samedi'
}

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
    tenant_df_avg = tenant_df.groupby(tenant_df['Température moyenne (°C)'], as_index=False)['kWh'].mean().round(2)
    homeowner_df_avg = homeowner_df.groupby(homeowner_df['Température moyenne (°C)'], as_index=False)['kWh'].mean().round(2)
    return tenant_df_avg, homeowner_df_avg

def avg_consumption_per_hour(tenant_df, homeowner_df):
    tenant_df_avg = tenant_df.copy()
    tenant_df_avg['Date et heure'] = tenant_df_avg['Date et heure'].str.slice(start=11, stop=13)
    tenant_df_avg = tenant_df_avg.groupby(tenant_df_avg['Date et heure'], as_index=False)['kWh'].mean().round(2)
    homeowner_df_avg = homeowner_df.copy()
    homeowner_df_avg['Date et heure'] = homeowner_df_avg['Date et heure'].str.slice(start=11, stop=13)
    homeowner_df_avg = homeowner_df_avg.groupby(homeowner_df_avg['Date et heure'], as_index=False)['kWh'].mean().round(2)
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
    avg_data_df = df.groupby(df['Saison'], as_index=False)[['kWh', 'Température moyenne (°C)']].mean().round(2)

    return avg_data_df

def group_days(df):
    days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    df = df.loc[:, ['Contrat', 'Date et heure', 'kWh']]

    df['Date et heure'] = pd.to_datetime(df['Date et heure'])
    
    day_df = df[df['Date et heure'].apply(is_daytime)]

    day_df = day_df.groupby([pd.Grouper(key='Date et heure', freq='D'), 'Contrat'])['kWh'].sum().reset_index()
    day_df['day_of_week'] = day_df['Date et heure'].dt.day_name().apply(lambda x: DAYS[str(x)])
    day_df = day_df.groupby(pd.Grouper(key='day_of_week'))['kWh'].mean().reset_index()
    day_df['day_of_week'] = pd.Categorical(day_df['day_of_week'], categories=days, ordered=True)
    day_df = day_df.sort_values('day_of_week')


    return day_df

def group_nights(df):
    days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    df = df.loc[:, ['Contrat', 'Date et heure', 'kWh']]
    df['Date et heure'] = pd.to_datetime(df['Date et heure'])

    night_df = df[~df['Date et heure'].apply(is_daytime)]

    night_df = night_df.groupby([pd.Grouper(key='Date et heure', freq='D'), 'Contrat'])['kWh'].sum().reset_index()
    night_df['day_of_week'] = night_df['Date et heure'].dt.day_name().apply(lambda x: DAYS[str(x)])
    night_df = night_df.groupby(pd.Grouper(key='day_of_week'))['kWh'].mean().reset_index()
    night_df['day_of_week'] = pd.Categorical(night_df['day_of_week'], categories=days, ordered=True)
    night_df = night_df.sort_values('day_of_week')

    return night_df

    
def is_daytime(dt):
    hour = dt.hour
    return 6 <= hour < 22
       
