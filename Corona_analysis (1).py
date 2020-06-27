
# coding: utf-8

# # Corona Virus Analysis 
#  By Anubhav Sharma

# ## Importing datasets

# In[132]:

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# In[133]:

df_confirmed=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
df_confirmed.head()


# In[134]:

df_recovered=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
df_recovered.head()


# In[135]:

df_death=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
df_death.head()


# In[136]:

df_cases=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
df_cases.head()


# In[137]:

print(df_confirmed.shape)
print(df_death.shape)
print(df_recovered.shape)
print(df_cases.shape)


# ## Data Preprocessing

# In[138]:

#All the first 3 datasets have same number of columns
df_confirmed.columns


# In[139]:

df_cases.isnull().sum()


# In[140]:

#let's see where we stand on Global level
df_global=df_cases.copy().drop({'Last_Update','Lat','Long_','Country_Region'},axis=1)
global_summary=pd.DataFrame(df_global.sum())


# In[141]:

global_summary=global_summary.transpose()
global_summary


# In[142]:

global_summary=global_summary.drop({'People_Tested','People_Hospitalized','Incident_Rate','UID'},axis=1)
global_summary.style.format("{:,.0f}")


# In[143]:

#Now we will visualize Covid 19 Clusters in the world
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors


import folium


# In[144]:

print(df_cases['Lat'].isnull().sum())
print(df_cases['Long_'].isnull().sum())


# In[145]:


df_cases[df_cases['Lat'].isnull()]


# In[146]:

df_cases=df_cases.drop(df_cases.index[[68,116]])
df_cases['Lat'].isnull().sum()


# ## Visualizing covid 19 across the world

# ### Most number of cases 
# We can see that most number of cases are in North and South America followed by India

# In[147]:

#total confirmed cases around the world
world_map_confirmed=folium.Map(location=[20,0],tiles='cartodbdark_matter',zoom_start=2)
for lat,lng,confirmed in zip(df_cases['Lat'],df_cases['Long_'],df_cases['Confirmed']):
    label='{}'.format(confirmed)
    label=folium.Popup(label,parse_html=True)
    folium.CircleMarker([lat,lng],
                       radius=confirmed/60000,
                       popup=label,
                        color='crimson',
                        fill_color='#DC143C ',
                        fill=True,
                        fill_opacity=0.7,
                        parse_html=False).add_to(world_map_confirmed)

world_map_confirmed


# ### Most Number of recoveries
# Here we can see many countries with good recovry number but most number of recoveries are in USA

# In[148]:

#Total Recovered Cases 
world_map_recovered=folium.Map(location=[20,0],tiles='cartodbdark_matter',zoom_start=2)
for lat,lng,recovered in zip(df_cases['Lat'],df_cases['Long_'],df_cases['Recovered']):
    label='{}'.format(recovered)
    label=folium.Popup(label,parse_html=True)
    folium.CircleMarker([lat,lng],
                       radius=recovered/50000,
                       popup=label,
                       color='#32CD32',
                       fill_color='#32CD32',
                       fill=True,
                       fill_opacity=0.7,
                       parse_html=False).add_to(world_map_recovered)
world_map_recovered


# ### Most number of deaths
# so here we can see an interesting visual which tells us that some countries who are not even in top 5 countries having most number of cases have signiificant amount of deaths. India on the other hand have managed to control death rate.

# In[149]:

#total number of deaths
world_map_death=folium.Map(location=[20,0],tiles='cartodbdark_matter',zoom_start=2)
for lat,lng,death in zip(df_cases['Lat'],df_cases['Long_'],df_cases['Deaths']):
    label='{}'.format(death)
    label=folium.Popup(label,parse_html=True)
    if(death==0):
        pass
    else:
        folium.CircleMarker([lat,lng],
                       
                       radius=death/5000,
                       popup=label,
                       color='red',
                       fill_color='red',
                       fill=True,
                       fill_opacity=0.7,
                       parse_html=False).add_to(world_map_death)
world_map_death


# In[150]:

ts_confirmed=pd.DataFrame(df_confirmed.sum()).transpose()
ts_confirmed


# ## Visualizing daily increase , recoveries and deaths of covid 19 around the world
# Here we will see that how have we done as a world in this pandemic

# In[151]:

ts_confirmed=ts_confirmed.drop({'Lat','Long'},axis=1)


# In[152]:

ts_confirmed=ts_confirmed.transpose()
ts_confirmed.head()


# In[153]:

ts_confirmed=ts_confirmed.reset_index()


# In[154]:

ts_confirmed.head()


# In[155]:

ts_confirmed=ts_confirmed.rename(columns={'index':'dates',0:'num_cases'})
ts_confirmed.head()


# In[156]:

import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go
pyo.init_notebook_mode()


# In[157]:

ts_recovered=pd.DataFrame(df_recovered.sum())
ts_recovered.head()


# In[158]:

ts_recovered=ts_recovered.drop({'Lat','Long'},axis=0)
ts_recovered=ts_recovered.reset_index()
ts_recovered=ts_recovered.rename(columns={'index':'dates',0:'recovered'})
ts_recovered.head()


# In[159]:

ts_death=pd.DataFrame(df_death.sum())
ts_death.head()


# In[160]:

ts_death=ts_death.drop({'Lat','Long'},axis=0)
ts_death=ts_death.reset_index()
ts_death=ts_death.rename(columns={'index':'dates',0:'deaths'})
ts_death.head()


# In[161]:

# Now we will create a dataframe for active
#series converts normal array into columns
ts_active=pd.Series(
    data=np.array(
    [x1-x2-x3 for (x1,x2,x3) in zip(ts_confirmed['num_cases'],ts_death['deaths'],ts_recovered['recovered'])]),index=ts_confirmed['dates'])


# In[162]:

ts_active=ts_active.reset_index()
ts_active.head()


# In[163]:

ts_active=ts_active.rename(columns={0:'active'})
ts_active.head()


# In[164]:

# Now we will visualize number of cases,active cases,total recoveries and total deaths
trace0=go.Scatter(
        x=ts_confirmed['dates'],
        y=ts_confirmed['num_cases'],
        mode='lines',
        name='Total num of cases')

trace1=go.Scatter(
        x=ts_recovered['dates'],
        y=ts_recovered['recovered'],
        mode='lines',
        name='Total recoveries')

trace2=go.Scatter(
        x=ts_death['dates'],
        y=ts_death['deaths'],
        mode='lines',
        name='Total deaths')

trace3=go.Scatter(
        x=ts_active['dates'],
        y=ts_active['active'],
        mode='lines',
        name='Total active cases')


# In[165]:

data=[trace0,trace1,trace2,trace3]
layout=go.Layout(title='Corona Virus scenario')
fig=go.Figure(data,layout)
fig.show()


# In[166]:

fig = px.bar(ts_confirmed, x="dates", y='num_cases', title="daily confirmed cases")
fig.show()


# ### Top 20 countrues with most number of cases

# In[167]:

#Now we will see top 20 countries
df_top20=df_cases.drop({'Last_Update','Lat','Long_','People_Hospitalized','Mortality_Rate','UID','ISO3'},axis=1)


# In[169]:

df_top20.sort_values(by='Confirmed',axis=0,ascending=False,inplace=True)


# In[170]:

df_top20=df_top20.head(20)


# In[171]:

df_top20.reset_index(drop=True,inplace=True)


# In[172]:

df_top20=df_top20.drop({'People_Tested'},axis=1)


# In[173]:

df_top20.style.bar(align='left',subset=['Confirmed', 'Deaths','Recovered','Active','Incident_Rate'], color='Red')


# ## Analysing the situation in India
# Now we will analyse the situation of coronavirus in India

# In[174]:

#Now we will Analyze India
df_india=pd.DataFrame(df_top20.loc[3,:])


# In[175]:

df_india=df_india.transpose()


# In[176]:

df_india.reset_index(drop=True,inplace=True)
df_india


# In[177]:

ts_confirmed_india=df_confirmed[df_confirmed['Country/Region'] == 'India']
ts_confirmed_india=ts_confirmed_india.drop({'Province/State','Lat','Long'},axis=1).reset_index(drop=True).sum()
ts_confirmed_india=ts_confirmed_india.to_frame()
ts_confirmed_india=ts_confirmed_india.drop(ts_confirmed_india.index[0])
ts_confirmed_india=ts_confirmed_india.reset_index()
ts_confirmed_india=ts_confirmed_india.rename(columns={'index':'dates',0:'confirmed'})
ts_confirmed_india.head()


# In[178]:

ts_recovered_india=df_recovered[df_recovered['Country/Region']=='India']
ts_recovered_india=ts_recovered_india.drop({'Province/State','Lat','Long'},axis=1).reset_index(drop=True).sum()
ts_recovered_india=ts_recovered_india.to_frame()
ts_recovered_india=ts_recovered_india.drop(ts_recovered_india.index[0])
ts_recovered_india=ts_recovered_india.reset_index()
ts_recovered_india=ts_recovered_india.rename(columns={'index':'dates',0:'recovered'})
ts_recovered_india.head()


# In[179]:

ts_death_india=df_death[df_death['Country/Region']=='India']
ts_death_india=ts_death_india.drop({'Province/State','Lat','Long'},axis=1).reset_index(drop=True).sum()
ts_death_india=ts_death_india.to_frame()
ts_death_india=ts_death_india.drop(ts_death_india.index[0])
ts_death_india=ts_death_india.reset_index()
ts_death_india=ts_death_india.rename(columns={'index':'dates',0:'deaths'})
ts_death_india.head()


# In[180]:

ts_active_india=pd.Series(
    data=np.array(
    [x1-x2-x3 for (x1,x2,x3) in zip (ts_confirmed_india['confirmed'],ts_death_india['deaths'],ts_recovered_india['recovered'])]),
    index=ts_confirmed_india['dates']
)
ts_active_india=ts_active_india.to_frame()
ts_active_india=ts_active_india.reset_index()
ts_active_india=ts_active_india.rename(columns={'index':'dates',0:'active'})
ts_active_india.head()


# In[181]:

trace0=go.Scatter(
        x=ts_confirmed_india['dates'],
        y=ts_confirmed_india['confirmed'],
        mode='lines',
        name='Total num of cases')

trace1=go.Scatter(
        x=ts_recovered_india['dates'],
        y=ts_recovered_india['recovered'],
        mode='lines',
        name='Total recoveries')

trace2=go.Scatter(
        x=ts_death_india['dates'],
        y=ts_death_india['deaths'],
        mode='lines',
        name='Total deaths')

trace3=go.Scatter(
        x=ts_active_india['dates'],
        y=ts_active_india['active'],
        mode='lines',
        name='Total active cases')


# ### Good rate of recovery
# Even though cases are increasing significantly but we have managed to flatten active cases curve and we are having good number of recoveries while supressing the death curve

# In[182]:

data=[trace0,trace1,trace2,trace3]
layout=go.Layout(title='Corona Virus scenario in India')
fig=go.Figure(data,layout)
fig.show()


# In[183]:

fig = px.bar(ts_confirmed_india, x="dates", y='confirmed', title="Daily confirmed cases")
fig.show()


# ## Analyising situation in various states across India

# In[184]:

#Now I will Analyze India's data state wise
india_state=pd.read_csv('https://raw.githubusercontent.com/imdevskp/covid-19-india-data/master/state_level_latest.csv')


# In[185]:

india_state.head()


# In[186]:

india_state.drop({'Last_Updated_Time','Migrated_Other','Delta_Confirmed','Delta_Recovered','Delta_Deaths','State_Notes'},
                axis=1,inplace=True)


# In[187]:

india_state.drop(india_state.index[[0,9]],inplace=True)
india_state=india_state.reset_index(drop=True)
india_state.style.bar(subset=['Confirmed','Recovered','Deaths','Active'],color='red')


# ## States with most number of cases

# In[188]:

#lets create a bar chart of top 5 States comparing the number of confirmed cases
df_bar=india_state.loc[0:4,['State','Confirmed']]


# In[189]:

df_bar.set_index('State',drop=True,inplace=True)


# In[190]:

df_bar.plot(kind='bar',figsize=(10,6),rot=90,color='orange')
plt.xlabel('States')
plt.ylabel('Total Confirmed Cases')
plt.title('Top 5 States with Most number of Confirmed Cases')

plt.show()


# ## States with most number of recoveries
# Here we see that though Tamil Nadu has more number of cases delhi is leading in number of recoveries

# In[191]:

#state with max recoveries
df_bar_recovered=india_state.loc[0:4,['State','Recovered']]
df_bar_recovered.set_index('State',drop=True,inplace=True)
df_bar_recovered.sort_values('Recovered',axis=0,ascending=False,inplace=True)


# In[192]:

df_bar_recovered.plot(kind='bar',figsize=(10,6),rot=90,color='green')
plt.xlabel('states')
plt.ylabel('Number of recoveries')
plt.title('States with Most recoveries')
plt.show()


# ## States with most number of deaths 
# Here we see that Tamil Nadu has managed to contain deaths even though having second most number of cases

# In[193]:

#State with Max deaths
df_bar_death=india_state.loc[0:4,['State','Deaths']]
df_bar_death.set_index('State',drop=True,inplace=True)
df_bar_death.sort_values('Deaths',axis=0,ascending=False,inplace=True)


# In[194]:

df_bar_death.plot(kind='bar',figsize=(10,6),rot=90,color='red')
plt.xlabel('states')
plt.ylabel('Number of deaths')
plt.title('States with Most Deaths')
plt.show()
#Tamil Nadu despite having Second largest cases is on 4th number in deaths


# ## Here we wil analyse the state with most number of cases per million

# In[195]:

import xlsxwriter
path=r'C:\Users\Anubhav\Untitled Folder\\Indian States Population and Area.xlsx'
df = pd.ExcelFile(path)


# In[196]:

df.sheet_names


# In[197]:

df_pop = df.parse("Sheet1")


# In[198]:

df_pop.head()
#I will use this data since we can't Rely on data of 2011 Census and this gives pretty basic Idea


# In[199]:

df_state_pop=pd.merge(india_state,df_pop,on='State')


# In[200]:

df_state_pop.rename(columns={'Aadhaar assigned as of 2019':'Population'},inplace=True)


# In[201]:

df_state_pop.head()


# In[202]:

df_state_pop['Cases/million']=(df_state_pop['Confirmed']/df_state_pop['Population'])*1000000
df_state_pop.sort_values('Cases/million',axis=0,ascending=False,inplace=True)
df_state_pop.reset_index(drop=True,inplace=True)
df_state_pop.drop({'Area (per sq km)'},axis=1,inplace=True)
df_state_pop.head()


# In[203]:

#We will visualize 5 states with most cases/million
df_bar_pop=df_state_pop.loc[0:4,['State','Cases/million']]
df_bar_pop.set_index('State',inplace=True)


# ### Here we see an interesting thing that compared to its population Delhi has a lot more cases as compared to Maharasthra

# In[204]:

df_bar_pop.plot(kind='bar',figsize=(10,6))
plt.xlabel('States')
plt.ylabel('Cases/million')
plt.title('States with most cases/million')
plt.show()


# In[205]:

import seaborn as sns
plt.figure(figsize = (12,8))
sns.heatmap(df_state_pop.corr(), annot=True)
plt.show()


# In[206]:

covid_daily=pd.read_csv('https://raw.githubusercontent.com/imdevskp/covid-19-india-data/master/state_level_daily.csv')


# In[207]:

covid_daily.head()


# ## We will here Analyse which state among top 6 has managed to flatten the curve

# In[208]:

#Now we will see top 6 states and which were able to flatten the curve
covid_maha=covid_daily[covid_daily['State']=='MH']
covid_maha=covid_maha.drop({'Deceased','Recovered','Unnamed: 0'},axis=1)
covid_maha['Date'] =pd.to_datetime(covid_maha.Date)
covid_maha.sort_values(by='Date',ascending=True,inplace=True)
covid_maha.reset_index(drop=True,inplace=True)
covid_maha.head()


# In[209]:

covid_del=covid_daily[covid_daily['State']=='DL']
covid_del=covid_del.drop({'Deceased','Recovered','Unnamed: 0'},axis=1)
covid_del['Date'] =pd.to_datetime(covid_del.Date)
covid_del.sort_values(by='Date',ascending=True,inplace=True)
covid_del.reset_index(drop=True,inplace=True)
covid_del.head()


# In[210]:

covid_guj=covid_daily[covid_daily['State']=='GJ']
covid_guj=covid_guj.drop({'Deceased','Recovered','Unnamed: 0'},axis=1)
covid_guj['Date'] =pd.to_datetime(covid_guj.Date)
covid_guj.sort_values(by='Date',ascending=True,inplace=True)
covid_guj.reset_index(drop=True,inplace=True)
covid_guj.head()


# In[211]:

covid_tn=covid_daily[covid_daily['State']=='TN']
covid_tn=covid_tn.drop({'Deceased','Recovered','Unnamed: 0'},axis=1)
covid_tn['Date'] =pd.to_datetime(covid_tn.Date)
covid_tn.sort_values(by='Date',ascending=True,inplace=True)
covid_tn.reset_index(drop=True,inplace=True)
covid_tn.head()


# In[212]:

covid_up=covid_daily[covid_daily['State']=='UP']
covid_up=covid_up.drop({'Deceased','Recovered','Unnamed: 0'},axis=1)
covid_up['Date'] =pd.to_datetime(covid_up.Date)
covid_up.sort_values(by='Date',ascending=True,inplace=True)
covid_up.reset_index(drop=True,inplace=True)
covid_up.head()


# In[213]:

covid_rj=covid_daily[covid_daily['State']=='RJ']
covid_rj=covid_rj.drop({'Deceased','Recovered','Unnamed: 0'},axis=1)
covid_rj['Date'] =pd.to_datetime(covid_rj.Date)
covid_rj.sort_values(by='Date',ascending=True,inplace=True)
covid_rj.reset_index(drop=True,inplace=True)
covid_rj.head()


# In[214]:

trace0=go.Scatter(
        x=covid_maha['Date'],
        y=covid_maha['Confirmed'],
        mode='lines',
        name='Cases in Maharashtra')

trace1=go.Scatter(
        x=covid_del['Date'],
        y=covid_del['Confirmed'],
        mode='lines',
        name='Cases in Delhi')

trace2=go.Scatter(
        x=covid_tn['Date'],
        y=covid_tn['Confirmed'],
        mode='lines',
        name='Cases in Tamil Nadu')

trace3=go.Scatter(
        x=covid_up['Date'],
        y=covid_up['Confirmed'],
        mode='lines',
        name='Cases in Uttar Pradesh')

trace4=go.Scatter(
        x=covid_rj['Date'],
        y=covid_rj['Confirmed'],
        mode='lines',
        name='Cases in Rajasthan')

trace5=go.Scatter(
        x=covid_guj['Date'],
        y=covid_guj['Confirmed'],
        mode='lines',
        name='Cases in Gujrat')


# ### Here we see that Rajasthan , Gujrat and Uttar Pradesh have almost managed to flatten their curve despite having a lot cases in beginning of pandemic

# In[215]:

data=[trace0,trace1,trace2,trace3,trace4,trace5]
layout=go.Layout(title='Which States are flattening Curve')
fig=go.Figure(data,layout)
fig.show()


# ## Analysing Medical scenario in various states

# In[216]:

# Now we will see which States are ready to face pandemic 
df_health=pd.read_csv(r'C:\Users\Anubhav\Untitled Folder\datasets_557629_1259476_HospitalBedsIndia.csv')
df_health.head()


# In[217]:

df_health.columns


# In[218]:

df_health=df_health.drop({'Sno','NumPrimaryHealthCenters_HMIS','NumCommunityHealthCenters_HMIS','NumSubDistrictHospitals_HMIS',
               'NumDistrictHospitals_HMIS','TotalPublicHealthFacilities_HMIS','NumRuralHospitals_NHP18',
                         'NumUrbanHospitals_NHP18'},axis=1)
df_health.head()


# In[219]:

df_health['Total Beds'] = df_health.loc[:,'NumPublicBeds_HMIS'].add(df_health.loc[:,'NumRuralBeds_NHP18']).add(df_health.loc[:,'NumUrbanBeds_NHP18'])


# In[220]:

df_health.drop({'NumPublicBeds_HMIS','NumRuralBeds_NHP18','NumUrbanBeds_NHP18'},axis=1,inplace=True)


# In[221]:

df_health=df_health.rename(columns={'State/UT':'State'})
df_health.head()


# In[222]:

df_state_health=pd.merge(df_state_pop,df_health,on='State')
df_state_health.head()


# In[223]:

#We can see that our top 5 affected states are not even in top 10 of beds/million index 
df_state_health['beds/million']=(df_state_health['Total Beds']/df_state_health['Population'])*1000000
df_state_health.sort_values('beds/million',axis=0,ascending=False,inplace=True)
df_state_health.reset_index(drop=True,inplace=True)
df_state_health


# In[224]:

df_bar_beds=df_state_health.loc[0:5,['State','beds/million']]
df_bar_beds.set_index('State',drop=True,inplace=True)
df_bar_beds.head()


# ### Not even one state from top 5 states having most number of cases is in top 10 states of most beds/ million which tells us that we were not ready to face this pandemic

# In[225]:

df_bar_beds.plot(kind='bar',figsize=(10,6))
plt.xlabel('States')
plt.ylabel('beds/million')
plt.title('States with most beds per million')
plt.show()


# In[ ]:



