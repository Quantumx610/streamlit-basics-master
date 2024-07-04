import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title= 'Startup Analysis') #tab me name change
df = pd.read_csv('startup_cleaned.csv')
st.sidebar.title('Startup Funding Analysis')

df['Date'] = pd.to_datetime(df['Date'],errors='coerce')
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

def load_overall_analysis():
    st.title('Overall analysis')
    col1,col2,col3,col4 = st.columns(4)
    #total invested amount

    total = round(df['Amount'].sum())
    with col1:   
        st.metric('Total', str(total)+'Cr')
    with col2:
        max_funding  = df.groupby('Startup')['Amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Maximum Funding', str(max_funding)+'Cr')
    with col3:
        avg_funding = round(df.groupby('Startup')['Amount'].sum().mean())
        st.metric('Avg. Funding', str(avg_funding)+'Cr')
    with col4:
        num_startups = df['Startup'].nunique()
        st.metric('Funded Startups',num_startups)

    #Month on month graph

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['Year', 'Month'])['Amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['Year', 'Month'])['Amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['Month'].astype('str') + '-' + temp_df['Year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['Amount'])
    plt.xticks(fontsize = 3)

    st.pyplot(fig3)

def load_startup_analysis(startup):


# Funding Rounds
# Stage
# Investors
# Date
# Similar company

    recent5inv = df[df['Startup'].str.contains(startup)].head()[['Date','Verticle','City','Investors','Amount']]
    st.subheader('Most recent investors')
    st.dataframe(recent5inv)

    st.subheader('Biggest investors')
    big_series = df[df['Startup'].str.contains(startup)].groupby('Investors')['Amount'].sum().sort_values(ascending= False).head()
    st.dataframe(big_series)

    fig, ax = plt.subplots()
    ax.bar(big_series.index,big_series.values)

    st.pyplot(fig)

    col1,col2 = st.columns(2)
    #biggest investmest
    with col1:
        #startup round
        startup_round = df[df['Startup'].str.contains(startup)][['Date','Round','Investors']]
        st.subheader('Startup Rounds')
        
        st.dataframe(startup_round)


    with col2:
        st.subheader('Stagewise investment')
        stg_inv = df[df['Startup'].str.contains(startup)].groupby('Round')['Amount'].sum()

        fig2 , ax2 = plt.subplots()
        ax2.pie(stg_inv,labels = stg_inv.index,autopct='%0.01f%%')
        st.pyplot(fig2)

    col3,col4 = st.columns(2)

    # #stage wise investment --> round
    # with col3:

    #     st.subheader('Stagewise investment')
    #     stg_inv = df[df['Startup'].str.contains(startup)].groupby('Round')['Amount'].sum()

    #     fig2 , ax2 = plt.subplots()
    #     ax2.pie(stg_inv,labels = stg_inv.index,autopct='%0.01f%%')
    #     st.pyplot(fig2)

    # #city wise investment
    # with col4:

    st.subheader('City wise investors')
    city_inv = df[df['Startup'].str.contains(startup)].groupby('City')['Amount'].sum()
    
    fig3 , ax3 = plt.subplots()
    ax3.pie(city_inv,labels = city_inv.index,autopct='%0.00001f%%')
    st.pyplot(fig3)


    

def load_investor_detail(investor):
    st.title(investor)
    recent5df = df[df['Investors'].str.contains(investor)].head()[['Date', 'Startup','Verticle','City','Round','Amount']]
    st.subheader('Most recent investments')
    st.dataframe(recent5df)
    col1,col2 = st.columns(2)
    #biggest investmest
    with col1:
        st.subheader('Biggest investment')
        big_series = df[df['Investors'].str.contains(investor)].groupby('Startup')['Amount'].sum().sort_values(ascending= False).head()
        st.dataframe(big_series)

        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series = df[df['Investors'].str.contains(investor)].groupby('Verticle')['Amount'].sum()
        st.subheader('Sectors invested in')
        fig1 , ax1 = plt.subplots()
        ax1.pie(vertical_series,labels = vertical_series.index,autopct='%0.01f%%')

        st.pyplot(fig1)

    col3,col4 = st.columns(2)

    #stage wise investment --> round
    with col3:

        st.subheader('Stagewise investment')
        stg_inv = df[df['Investors'].str.contains(investor)].groupby('Round')['Amount'].sum()

        fig2 , ax2 = plt.subplots()
        ax2.pie(stg_inv,labels = stg_inv.index,autopct='%0.01f%%')
        st.pyplot(fig2)

    #city wise investment
    with col4:

        st.subheader('City wise investments')
        city_inv = df[df['Investors'].str.contains(investor)].groupby('City')['Amount'].sum()
        
        fig3 , ax3 = plt.subplots()
        ax3.pie(city_inv,labels = city_inv.index,autopct='%0.01f%%')
        st.pyplot(fig3)

#YOY Investment

    st.subheader('YoY investments')

    df['Year'] = df['Date'].dt.year
    yoy = df[df['Investors'].str.contains(investor)].groupby('Year')['Amount'].sum()
    
    fig4 , ax4 = plt.subplots()
    ax4.plot(yoy.index, yoy.values)
    st.pyplot(fig4,clear_figure= True)

#similar investors (to add)

option = st.sidebar.selectbox('Select', ['Overall Analysis','Startup','Investor'])

if option== 'Overall Analysis':
    load_overall_analysis()
elif option== 'Startup':
    selected_startup = st.sidebar.selectbox('select startup',sorted(df['Startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:    
        st.title('Startup Analysis')
        load_startup_analysis(selected_startup)

else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['Investors'].str.split(',').sum())))
    
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        st.title('Investor Analysis')
        load_investor_detail(selected_investor)
    