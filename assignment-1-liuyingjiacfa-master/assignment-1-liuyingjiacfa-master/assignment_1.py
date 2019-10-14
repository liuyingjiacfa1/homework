import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pylab import mpl,plt
plt.style.use('ggplot')
mpl.rcParams['font.family']='serif'

data={
'url1':"https://www.ncdc.noaa.gov/cag/statewide/time-series/",
'url2':"-tavg-1-",
'url3':"-1895-2019.csv?base_prd=true&begbaseyear=1901&endbaseyear=2000",
'path':r'C:\LYJ\Python\homework\assignment-1-liuyingjiacfa-master\weather',
'save_path':r'C:\Users\Yingj\Desktop\Data Homework\homework\assignment-1-liuyingjiacfa-master',
'plot_state':['Illinois','California','New York','Texas']
}

class Homework1():
    def __init__(self, data):
        self.url1 = data['url1']
        self.url2 = data['url2']
        self.url3 = data['url3']
        self.path = data['path']
        self.save_path = data['save_path']
        self.plot_state = data['plot_state']
        
        urls=[]
        for i in range(1,49):
            for j in [1,8]:
                url=self.url1+str(i)+self.url2+str(j)+self.url3
                urls.append(url)

        for url in urls:
            response = requests.get(url)
            state, measure, month = response.text.split('\n')[0].split(', ')
            with open(os.path.join(self.path, state + '_' + month + '.csv'), 'w') as ofile:
                ofile.write(response.text)
        weather_data = os.listdir(self.path)

        dfs = []
        for f in weather_data:
            st, month = f.split('_')
            df = pd.read_csv(os.path.join(self.path, f), skiprows = 4)
            df['State'] = st
            df['Date'] = pd.to_datetime(df['Date'], format = '%Y%m')
            dfs.append(df)
        
        df = pd.concat(dfs)
        df = df.sort_values(['State', 'Date'])
        
        self.df = df
    
    def plot_1(self):

        self.df['Year'] = self.df['Date'].map(lambda d: d.year)
        self.df['Jan-Aug Delta'] = self.df.groupby(['State', 'Year'])['Value'].diff()
        df_delta = self.df.dropna(subset=['Jan-Aug Delta'])[['State', 'Year', 'Jan-Aug Delta']]
        
        State = []
        for name, group in df_delta.groupby('State'):
            State.append(name)
        
        df_delta2 = pd.DataFrame()
        for state in State :
            df_delta2['Year']=df_delta['Year'][:125]
            df_delta2[state]=df_delta[df_delta['State']==state].iloc[:,2]
        df_delta2.index=df_delta2['Year']
        
        title_name = 'Average Jan-Aug Temperature Variation'
        df_delta2.loc[:, self.plot_state].plot(subplots = True, figsize = (16,9),title = title_name)
        plt.savefig(self.save_path + '\Jan_Aug_Temp_Delta.png')

    def plot_2(self):
        self.df['Month'] = self.df['Date'].map(lambda d: d.month)
        df2 = self.df.dropna()
        
        State2 = []
        for name, group in df2.groupby('State'):
            State2.append(name)
       
        df_average_temp = pd.DataFrame()
        for state in State2:
            df_average_temp['Year'] = df2['Year'][:125]
            df_average_temp[state] = df2[df2['State'] == state].iloc[:,1]
        df_average_temp.index = df_average_temp['Year']
        
        title_name = 'Average August Temperature'
        df_average_temp.loc[:,self.plot_state].plot(figsize = (16,9), title = title_name)
        plt.savefig(self.save_path + '\Aug_Temp.png')

Homework = Homework1(data)
Homework.plot_1()
Homework.plot_2()


