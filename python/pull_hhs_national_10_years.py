
# coding: utf-8

# <p>Class:  USC Viterbi Data Analytics Bootcamp</p>
# <p>Team:  Analyticus (aka Team 5)</p>
# <p>Module:  pull_hhs_national_10_years.py</p>
# <p>Version:  March 31, 2018</p>
# <p>Input:  HHS Vaccinations for six years for HHS API.</p>
# <p>Output:  HHS Vaccinations Json File for six years.</p>

# In[3]:


# Import Dependencies
import requests
import json
import numpy as np
import pandas as pd


# In[4]:


# Build a HHS dataframe for multiple API calls. 
# One call per year.
df1 = pd.DataFrame()
year_list = [2012, 2013, 2014, 2015, 2016, 2017]
for year_entry in year_list:
    url = "https://fluvaccineapi.hhs.gov/api/v2/vaccination_rates/trends/{}/national.json?ethnicity=T&medicare_status=A".format(year_entry)
    national_dict = requests.get(url).json()
    df = pd.DataFrame(national_dict)
    df1 = df1.append(df, ignore_index=True)


# In[5]:


# Inspect the HHS data, just downloaded into a dataframe.
df1.head()


# In[6]:


# Save the raw HHS data to a file as a save point.
df1.to_json('../data/raw_hhs_data.json')


# In[7]:


# Read the file just created into a dataframe.
# This services as a checkpoint in the process.
df2 = pd.read_json('../data/raw_hhs_data.json')


# In[8]:


# Inspect the HHS data.
df2.head()


# In[9]:


# Select only the attributes needed.
df3 = df2[['count', 'percentage', 'year', 'week']]


# In[10]:


# Rename columns to match the CCD data, vac_percent for eligible population
df4 = df3.rename(columns={"count":"vaccinations", "percentage":"vac_percent"})


# In[11]:


# Sort the HHS data by year and week to aid in analysis.
df5 = df4.sort_values(by=['year', 'week'])


# In[12]:


# Inspect HHS data.
df5.head()


# In[13]:


# Inspect HHS data.
df5.tail()


# In[14]:


# Add a "vaccinations percent by week" attribute to the HHS data.
df5['vac_pct_week'] = 0.0


# In[15]:


# Convert the vaccination percentage from a ration to a percentage.
df5['vac_percent'] = df5['vac_percent'] * 100


# In[16]:


# Inspect the HHS dataframe.
df5.head()


# In[17]:


# Calculate vaccination rate percentage per week 
# by finding the difference in the culmulative vaccination
# rate between weeks. Loop through week
for index_entry in df5.index:
    if df5.loc[index_entry, 'week'] == 1:
        df5.loc[index_entry, 'vac_pct_week'] = df5.loc[index_entry, 'vac_percent']
    elif index_entry > 0:
        i = index_entry - 1
        df5.loc[index_entry, 'vac_pct_week'] = df5.loc[index_entry, 'vac_percent'] - df5.loc[i, 'vac_percent']


# In[19]:


# Inspect the HHS dataframe for the calculated vaccination rate per week.
df5.tail()


# In[20]:


# Write the HHS data for ten years at the national level to a json file.
df5.to_json('../data/hhs_national_10_years.json')


# In[21]:


# Validate the above file by loading it into a dataframe.
df6 = pd.read_json('../data/hhs_national_10_years.json')


# In[22]:


# Sort the HHS data into year, week sequence to aid in inspection.
df7 = df6.sort_values(['year', 'week'])


# In[23]:


# Inspect the HHS data.
df7.head()


# In[24]:


# Inspect the HHS data.
df7.tail()

