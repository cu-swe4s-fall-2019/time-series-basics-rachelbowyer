import numpy as np
import pandas as pd
import datetime as dt

if __name__ == "__main__":
    activity = pd.read_csv('./smallData/activity_small.csv')
    activity = activity.loc[:, ~activity.columns.str.contains('^Unnamed')]
    activity['time'] = pd.to_datetime(activity['time'])
    activity['value'] = pd.to_numeric(activity['value'], errors='coerce')
    activity = activity.dropna()

    activity = activity.rename(columns={'value': 'activity'})
    activity = activity.set_index('time')

    # print(activity)
    # print(activity.dtypes)

    basal = pd.read_csv('./smallData/basal_small.csv')
    basal = basal.loc[:, ~basal.columns.str.contains('^Unnamed')]
    basal['time'] = pd.to_datetime(basal['time'])
    basal['value'] = pd.to_numeric(basal['value'], errors='coerce')
    basal = basal.dropna()

    basal = basal.rename(columns={'value': 'basal'})
    basal = basal.set_index('time')

    # print(basal)
    # print(basal.dtypes)

    bolus = pd.read_csv('./smallData/bolus_small.csv')
    bolus = bolus.loc[:, ~bolus.columns.str.contains('^Unnamed')]
    bolus['time'] = pd.to_datetime(bolus['time'])
    bolus['value'] = pd.to_numeric(bolus['value'], errors='coerce')
    bolus = bolus.dropna(thresh=2)

    bolus = bolus.rename(columns={'value': 'bolus'})
    bolus = bolus.set_index('time')

    # print(bolus)
    # print(bolus.dtypes)

    cgm = pd.read_csv('./smallData/cgm_small.csv')
    cgm = cgm.loc[:, ~cgm.columns.str.contains('^Unnamed')]
    cgm['time'] = pd.to_datetime(cgm['time'])
    cgm['value'] = pd.to_numeric(cgm['value'], errors='coerce')
    cgm = cgm.dropna()

    cgm = cgm.rename(columns={'value': 'cgm'})
    cgm = cgm.set_index('time')

    # print(cgm)
    # print(cgm.dtypes)

    hr = pd.read_csv('./smallData/hr_small.csv')
    hr = hr.loc[:, ~hr.columns.str.contains('^Unnamed')]
    hr['time'] = pd.to_datetime(hr['time'])
    hr['value'] = pd.to_numeric(hr['value'], errors='coerce')
    hr = hr.dropna()

    hr = hr.rename(columns={'value': 'hr'})
    hr = hr.set_index('time')

    # print(hr)
    # print(hr.dtypes)

    meal = pd.read_csv('./smallData/meal_small.csv')
    meal = meal.loc[:, ~meal.columns.str.contains('^Unnamed')]
    meal['time'] = pd.to_datetime(meal['time'])
    meal['value'] = pd.to_numeric(meal['value'], errors='coerce')
    meal = meal.dropna()

    meal = meal.rename(columns={'value': 'meal'})
    meal = meal.set_index('time')

    # print(meal)
    # print(meal.dtypes)

    smbg = pd.read_csv('./smallData/smbg_small.csv')
    smbg = smbg.loc[:, ~smbg.columns.str.contains('^Unnamed')]
    smbg['time'] = pd.to_datetime(smbg['time'])
    smbg['value'] = pd.to_numeric(smbg['value'], errors='coerce')
    smbg = smbg.dropna()

    smbg = smbg.rename(columns={'value': 'smbg'})
    smbg = smbg.set_index('time')

    # print(smbg)
    # print(smbg.dtypes)
    # print(smbg.index)

    framelist = [basal, bolus, hr, meal, smbg]
    newframe = cgm.join(activity, on='time', how='left')
    for frame in framelist:
        newframe = newframe.join(frame, on='time', how='left',
                                 lsuffix='_left', rsuffix='_right')

    newframe = newframe.fillna(0)
    newframe['time5'] = pd.Series(newframe.index.round('5min'),
                                  index=newframe.index)
    newframe['time15'] = pd.Series(newframe.index.round('15min'),
                                   index=newframe.index)
    # print(newframe)
    # print(newframe.loc['2018-03-16 18:44:00','activity'])

    grouped_sum_5 = newframe.groupby('time5').sum()
    grouped_avg_5 = newframe.groupby('time5').mean()

    want_5 = pd.Series(grouped_sum_5['activity'], index=grouped_sum_5.index)
    want_5 = pd.DataFrame(want_5, columns=['activity'])
    want_5['bolus'] = pd.Series(grouped_sum_5['bolus'],
                                index=grouped_sum_5.index)
    want_5['meal'] = pd.Series(grouped_sum_5['meal'],
                               index=grouped_sum_5.index)
    want_5['smbg'] = pd.Series(grouped_avg_5['smbg'],
                               index=grouped_avg_5.index)
    want_5['hr'] = pd.Series(grouped_avg_5['hr'],
                             index=grouped_avg_5.index)
    want_5['cgm'] = pd.Series(grouped_avg_5['cgm'],
                              index=grouped_avg_5.index)
    want_5['basal'] = pd.Series(grouped_avg_5['basal'],
                                index=grouped_avg_5.index)

    # print(want_5)
    # print(want_5.loc['2018-03-16 18:45:00',:])

    grouped_sum_15 = newframe.groupby('time15').sum()
    grouped_avg_15 = newframe.groupby('time15').mean()
    # print(grouped)

    want_15 = pd.Series(grouped_sum_15['activity'], index=grouped_sum_15.index)
    want_15 = pd.DataFrame(want_15, columns=['activity'])
    want_15['bolus'] = pd.Series(grouped_sum_15['bolus'],
                                 index=grouped_sum_15.index)
    want_15['meal'] = pd.Series(grouped_sum_15['meal'],
                                index=grouped_sum_15.index)
    want_15['smbg'] = pd.Series(grouped_avg_15['smbg'],
                                index=grouped_avg_15.index)
    want_15['hr'] = pd.Series(grouped_avg_15['hr'],
                              index=grouped_avg_15.index)
    want_15['cgm'] = pd.Series(grouped_avg_15['cgm'],
                               index=grouped_avg_15.index)
    want_15['basal'] = pd.Series(grouped_avg_15['basal'],
                                 index=grouped_avg_15.index)

    # print(want_15)

    want_5.to_csv('5min_binned_data.csv')
    want_15.to_csv('15min_binned_data.csv')
