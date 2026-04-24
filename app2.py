import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

#----------------load data----------------------
df= pd.read_csv("newfile.csv")
#-----------------Navbar-------------------------

select =option_menu(
    menu_title=None,
    options=["Home","Player Analysis","Country Insights","Comparison","Data Explorer"],
    icons=["house","person","globe","bar-chart","table"],
    orientation="horizontal"
)

#-----------------Home-------------------------
if select =="Home":
    st.title("Cricket Analysis Dashboard")

    col1,col2,col3,col4=st.columns(4)

    col1.metric("Total Players",df["Player"].nunique())

    col2.metric("Total Matches",df["Matches"].sum())

    col3.metric("Total Runs",df["Runs"].sum())
    
    col4.metric("Countries",df["Country"].nunique())
    st.dataframe(df.head()) 
#-----------------Player Analysis-------------------------
elif select=="Player Analysis":
    st.title("Player Analysis")
    player=st.selectbox("Select Player", df["Player"].unique())
    player_data=df[df["Player"]==player]

    stats =["100","50","6s","4s","0"]



    chart_data=(player_data[stats].iloc[0].reset_index()) #its converting data from series to core data frame
    chart_data.columns=["stat","Value"]

    fig=px.bar(
        chart_data,
        x="stat",
        y="Value",
        title="Player Performance"
    )
    st.plotly_chart(fig)
    fig2=px.bar(
        player_data,
        y=["100","50","6s","4s","0"],
        x="Matches",
        title="Player Performance"
    )
    st.plotly_chart(fig2)

    #-----------------Country Insights-------------------------
elif select=="Country Insights":
    st.title("country Insights")

    scountry=st.selectbox("Select Country",df["Country"].unique())
    
    col1,col2,col3,col4=st.columns(4)
    
    cdata=df[df["Country"]==scountry]

    players=df["Player"].nunique()
    total_runs=cdata["Runs"].sum()
    total_matches=cdata["Matches"].sum()
    total_innings=cdata["innings"].sum()
        #total runs
    col1.metric("Total Players",cdata["Player"].nunique())
    col2.metric('Total Runs',total_runs)
    col3.metric('Total Matches',total_matches)
    col4.metric('Total innings',total_innings)


    df2=cdata[['Player','Runs']]

    df3=cdata[['Player','Runs','Matches','100','6s']]
    df4=['Runs','Matches','100','6s']

    fig=px.pie(df2,names='Player',values='Runs')

    selectc=st.selectbox('select choice',df4)

    fig2=px.bar(df3,x='Player',y=selectc)

    col1,col2=st.columns(2)

    with col1:
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        st.plotly_chart(fig2,use_container_width=True)




   # st.plotly_chart(fig,use_container_width=True)
   #------------player comparison
elif select=='Comparison':
    st.title('Player comparison')

    players=st.multiselect(

        'compare player',
        df['Player'],
        default=df['Player'].head(5)
    )

    compare=df[df['Player'].isin(players)]

    fig=px.scatter(
        compare,
        x='Strike_rate',
        y='Ave',
        size='Runs',
        color='Country',
        hover_name='Player'
    )
    st.plotly_chart(fig,use_container_width=True)



elif select== 'Data Explorer':
    st.title('data Explorer')
    st.dataframe(df)
