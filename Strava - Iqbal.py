#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# In[5]:



auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

#replace variables with values for your account
payload = {
    'client_id': "73017",
    'client_secret': 'a5ad0c7f444309450219c6d68e6eb4b28d16aee3',
    'refresh_token': '19008dfe99c7d02096c719173dd2fe3f0a8d7ac3',
    'grant_type': "refresh_token",
    'f': 'json'
}


# In[6]:


print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))


# In[7]:


header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

print(my_dataset[0]["name"])
print(my_dataset[0]["map"]["summary_polyline"])


# In[14]:


import pandas as pd
from pandas import json_normalize

activities = json_normalize(my_dataset)

#Create new dataframe with only columns I care about
cols = ['name', 'upload_id', 'type', 'distance', 'moving_time',   
         'average_speed', 'max_speed','total_elevation_gain',
         'start_date_local'
       ]

activities = activities[cols]

#Break date into start time and date
activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
activities['start_time'] = activities['start_date_local'].dt.time
activities['start_date_local'] = activities['start_date_local'].dt.date

activities.head(5)

activities['type'].value_counts()

import seaborn as sns

runs = activities.loc[activities['type'] == 'Run'] 
runs.head(5)
sns.set(style="ticks", context="talk")
sns.scatterplot(x='distance', y = 'average_speed', data = runs).set_title("Average Speed vs Distance")

sns.scatterplot(x='distance', y = 'max_speed', data = runs).set_title("Max Speed vs Distance")


# In[16]:


import matplotlib.pyplot as plt
import numpy as np

#max speed over time
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.asarray(runs.start_date_local)
y = np.asarray(runs.max_speed)
ax.plot_date(x, y)
ax.set_title('Max Speed over Time')
fig.autofmt_xdate(rotation=45)
fig.tight_layout()


fig = plt.figure()
ax1 = fig.add_subplot(111)
x = np.asarray(runs.start_date_local)
y = np.asarray(runs.average_speed)
ax1.plot_date(x, y)
ax1.set_title('Average Speed over Time')
fig.autofmt_xdate(rotation=45)
fig.tight_layout()


# In[ ]:




