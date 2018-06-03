
# coding: utf-8

# <p>Class:  USC Viterbi Data Analytics Bootcamp</p>
# <p>Team:  Analyticus (aka Team 5)</p>
# <p>Module:  pull_hhs_state_data.py</p>
# <p>Version:  March 31, 2018</p>
# <p>Input:  HHS Vaccinations by state from HHS API for flu season 2017</p>
# <p>Output:  HHS Vaccinations Json File for flu season 2017.</p>

# In[1]:


# Import Dependencies
import requests
import json
import numpy as np
import pandas as pd


# In[2]:


# Format the URL to get state codes.
url = "https://fluvaccineapi.hhs.gov/api/v2/ids/2017/states.json"


# In[3]:


# Create the lsit of state codes, removing Distict of Columbia and Puerto Rico.
# Analysis will only include continental 50 states
state_codes = requests.get(url).json()
state_codes.remove('DC')
state_codes.remove('PR')


# In[4]:


# Build a list of state vaccination data.
results = []

for state_code in state_codes:
    
    url = "https://fluvaccineapi.hhs.gov/api/v2/vaccination_rates/trends/2017/states/{}.json?ethnicity=T&medicare_status=A".format(state_code)
    
    state_list = requests.get(url).json()
    
    for i in np.arange(0, len(state_list)):
        results.append(state_list[i])


# In[5]:


# Load a dataframe with the HHS data.
df = pd.DataFrame(results)


# In[6]:


# Inspect the HHS dataframe.
df.head()


# In[7]:


# Write the HHS data to a json file.
df.to_json('../data/hhs_state.json')


# In[8]:


# Start the file validation process by loading the file into a dataframe.
df1 = pd.read_json('../data/hhs_state.json')


# In[10]:


# Sort HHS data into state and week sequence to aid in inspection.
df2 = df1.sort_values(by=['name', 'week'])


# In[11]:


# Inspect the HHS data.
df2.head()


# In[12]:


# Inspect the HHS data.
df2.tail()

