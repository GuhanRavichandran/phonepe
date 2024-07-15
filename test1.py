import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px
import requests as rq
import json 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1997",
  auth_plugin='mysql_native_password',
  database='phonepe'
)
mycursor=mydb.cursor()
mycursor.execute("use phonepe")
mycursor.execute("select * from aggregate_insurance")
ag_ins=mycursor.fetchall()
column_names = [desc[0] for desc in mycursor.description]
Aggre_insu=pd.DataFrame(ag_ins,columns=mycursor.column_names)
mydb.commit()

mycursor.execute("select * from aggregate_transaction")
ag_trn=mycursor.fetchall()
column_names = [desc[0] for desc in mycursor.description]
Aggre_trns=pd.DataFrame(ag_trn,columns=mycursor.column_names)
mydb.commit()

mycursor.execute("select * from aggregate_User")
ag_user=mycursor.fetchall()
column_names = [desc[0] for desc in mycursor.description]
Aggre_users=pd.DataFrame(ag_user,columns=mycursor.column_names)
mydb.commit()


mycursor.execute("select * from map_insurance")
map_ins=mycursor.fetchall()
column_names = [desc[0] for desc in mycursor.description]
map_insu=pd.DataFrame(map_ins,columns=mycursor.column_names)
mydb.commit()


mycursor.execute("select * from map_transaction")
map_trn=mycursor.fetchall()
column_names = [desc[0] for desc in mycursor.description]
map_trns=pd.DataFrame(map_trn,columns=mycursor.column_names)
mydb.commit()


mycursor.execute("select * from map_user")
map_user=mycursor.fetchall()
column_names = [desc[0] for desc in mycursor.description]
map_users=pd.DataFrame(map_user,columns=mycursor.column_names)
mydb.commit()

mycursor.execute("select * from top_insurance")
top_ins=mycursor.fetchall()
column_names = [desc[0] for desc in mycursor.description]
top_insu=pd.DataFrame(top_ins,columns=mycursor.column_names)
mydb.commit()

mycursor.execute("select * from top_transaction")
top_trn=mycursor.fetchall()
column_names = [desc[0] for desc in mycursor.description]
top_trns=pd.DataFrame(top_trn,columns=mycursor.column_names)
mydb.commit()


mycursor.execute("select * from  top_user")
top_user=mycursor.fetchall()
column_names = [desc[0] for desc in mycursor.description]
top_users=pd.DataFrame(top_user,columns=mycursor.column_names)
mydb.commit()

def Transaction_year(df, year):
    Table_year=df[df["Years"]==year]
    Table_year.reset_index(drop=True,inplace=True)

    Table_group=Table_year.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Table_group.reset_index(inplace=True)
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = rq.get(url)
    data = json.loads(response.content)
    state_list = []
    for feature in data["features"]:
        state_list.append(feature["properties"]["ST_NM"])
    state_list.sort()
    
    column1,column2=st.columns(2)
    
    with column1:
        fig_amount=px.bar(Table_group,x="States",y="Transaction_amount",title=f"Transaction_Amount_{year}",color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount)
        
        fig_india = px.choropleth(Table_group, geojson=data, locations="States", featureidkey="properties.ST_NM",
                            color="Transaction_amount", color_continuous_scale="turbid",
                            range_color=(Table_group["Transaction_amount"].min(), Table_group["Transaction_amount"].max()),
                            hover_name="States", title=f"Transaction Amount {year}", fitbounds="locations",
                            height=600, width=600)
    
        st.plotly_chart(fig_india)
        
    with column2:
        fig_count=px.bar(Table_group,x="States",y="Transaction_count",title=f"Transaction_Count_{year}",color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_count)
    
        fig_india1=px.choropleth(Table_group, geojson=data, locations="States",featureidkey="properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="ylorbr",
                                    range_color=(Table_group["Transaction_count"].min(),Table_group["Transaction_count"].max()),
                                    hover_name="States",title=f"Transaction_Count {year}",fitbounds="locations",
                                    height=600,width=600)
        st.plotly_chart(fig_india1)
        
    return Table_year
        
def Transaction_Quarter(df, Quarter):
    Table_Quarter=df[df["Quarter"]==Quarter]
    Table_Quarter.reset_index(drop=True,inplace=True)

    Table_group= Table_Quarter.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Table_group.reset_index(inplace=True)
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = rq.get(url)
    data = json.loads(response.content)
    state_list = []
    for feature in data["features"]:
        state_list.append(feature["properties"]["ST_NM"])
    state_list.sort()
    
    column1,column2=st.columns(2)
    
    with column1:
        fig_amount=px.bar(Table_group,x="States",y="Transaction_amount",title=f"{Tran_year["Years"].max()} Transaction_Amount_in_Qtr{Quarter}",color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount)
        
        fig_india=px.choropleth(Table_group, geojson=data, locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="turbid",
                                range_color=(Table_group["Transaction_amount"].min(),Table_group["Transaction_amount"].max()),
                                hover_name="States",title=f"{Tran_year["Years"].max()} Transaction_Amount_in_Qtr_ {Quarter}",fitbounds="locations",
                                height=600,width=600)
        
        st.plotly_chart(fig_india)
    
    with column2:
        fig_count=px.bar(Table_group,x="States",y="Transaction_count",title=f"{Tran_year["Years"].max()} Transaction_Count_in_Qrt{Quarter}",color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_count)

        fig_india1=px.choropleth(Table_group, geojson=data, locations="States",featureidkey="properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="ylorbr",
                                    range_color=(Table_group["Transaction_count"].min(),Table_group["Transaction_count"].max()),
                                    hover_name="States",title=f"{Tran_year["Years"].max()} Transaction_Count_in_Qtr_ {Quarter}",fitbounds="locations",
                                    height=600,width=600)
        st.plotly_chart(fig_india1)

def Transaction_type(df,state):   
    Table_year=df[df["States"]==state]
    Table_year.reset_index(drop=True,inplace=True)   
    Table_group=Table_year.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    Table_group.reset_index(inplace=True)
    column1,column2=st.columns(2)
    with column1:
        fig_pie=px.pie(data_frame=Table_group, names="Transaction_type",values="Transaction_amount",width=600,title=f"Transaction_amount_in_{state}")
        st.plotly_chart(fig_pie)
    with column2:
        fig_pie1=px.pie(data_frame=Table_group, names="Transaction_type",values="Transaction_count",width=600,title=f"Transaction_count_in_{state}")
        st.plotly_chart(fig_pie1)
        
def user_brand(df, year):
    Table_user=df[df["Years"]==year]
    Table_user.reset_index(drop=True,inplace=True)
    
    user_group=pd.DataFrame(Table_user.groupby("Brands")["Transaction_count"].sum())
    user_group.reset_index(inplace=True)
    
    fig_bar=px.bar(user_group,x="Brands",y="Transaction_count",title=f"Brands and Transaction count in {year}",
                   width=600,color_discrete_sequence=px.colors.sequential.Blackbody,hover_name="Brands")
    st.plotly_chart(fig_bar)
    
    return Table_user
    
def user_quarter(df,Quarter):
    Table_user=df[df["Quarter"]==Quarter]
    Table_user.reset_index(drop=True,inplace=True)

    user_group=pd.DataFrame(Table_user.groupby("Brands")["Transaction_count"].sum())
    user_group.reset_index(inplace=True)

    fig_bar=px.bar(user_group,x="Brands",y="Transaction_count",title=f"Brands and Transaction count in Qtr {Quarter}",
                width=600,color_discrete_sequence=px.colors.sequential.Bluyl_r)
    st.plotly_chart(fig_bar)
    
def user_state(df,state):
    Brand_state=df[df["States"]==state]
    Brand_state.reset_index(drop=True,inplace=True)
    
    fig_bar=px.bar(Brand_state,x="Brands",y="Transaction_count",hover_data="Percentage",
                     title=f"Sales percentage by brands in {state}",width=600)
    st.plotly_chart(fig_bar)
    
def District_type(df,state):   
    Table_year=df[df["States"]==state]
    Table_year.reset_index(drop=True,inplace=True)   
    Table_group=Table_year.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    Table_group.reset_index(inplace=True)
    column1,column2=st.columns(2)
    with column1:
        fig_bar=px.bar(Table_group,x="Transaction_amount",y="Districts",title=f"Transaction_amount_in_{state}",color_discrete_sequence=px.colors.sequential.Brwnyl_r)
        st.plotly_chart(fig_bar)
        
    with column2:

        fig_bar1=px.bar(Table_group,x="Transaction_count",y="Districts",title=f"Transaction_count_in_{state}",color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_bar1)
        
def state_sale(df,year):   
    sale_year=df[df["Years"]==year]
    sale_year.reset_index(drop=True,inplace=True) 
    sale_group=sale_year.groupby("States")[["Registered_users","App_open"]].sum()
    sale_group.reset_index(inplace=True)  
    
    fig_graph=px.line(sale_group,x="States",y=["Registered_users","App_open"],title=f" RegisteredUsers and Appopens in {year}",markers=True)
    st.plotly_chart(fig_graph)
    
def Quarter_user(df,quarter):   
    sale_year=df[df["Quarter"]==quarter]
    sale_year.reset_index(drop=True,inplace=True) 
    sale_group=sale_year.groupby("States")[["Registered_users","App_open"]].sum()
    sale_group.reset_index(inplace=True)  
    
    fig_amount=px.line(sale_group,x="States",y=["Registered_users","App_open"],title=f" RegisteredUsers and Appopens in Qtr {quarter}",color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    st.plotly_chart(fig_amount)
    
def District_user(df,state):   
    sale_year=df[df["States"]==state]
    sale_year.reset_index(drop=True,inplace=True) 
    fig_amount=px.bar(sale_year,x="Registered_users",y="Districts",title=f" RegisteredUsers and Appopens in {state}",color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    st.plotly_char(fig_amount)


st.title(":violet[PHONEPE DATA VISUALIZATION AND EXPLORATION]")
st.caption(":blue[Insights of people transactions]:earth_asia:")
st.subheader(":green[This project gives data of transactions applied from different states ]")

import base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
background_image_path = r'C:\Users\Hp\OneDrive\Desktop\demo.py\phonepe.jpg'
base64_image = get_base64_of_bin_file(background_image_path)
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{base64_image}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# Main analysis options
analysis_options = st.radio("Select the Options", ("PHONEPE_ANALYSIS","DATA_EXPLORATION"))

if analysis_options == "PHONEPE_ANALYSIS":
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        

     col3,col4= st.columns(2)
    
    with col3:
        

     with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")


# Analysis sections
if analysis_options == "DATA_EXPLORATION":
    with st.expander("Aggregate Analysis"):
        show_trn_analysis = st.radio("Select the Analysis", ["Aggregate_Insurance_Analysis", "Aggregate_Transaction_Analysis", "Aggregate_User_Analysis"])
        st.write("Your selected analysis:", show_trn_analysis)
        
        if show_trn_analysis == "Aggregate_Insurance_Analysis":
            year = st.selectbox("Select the Year", Aggre_insu["Years"].unique())
            Tran_year = Transaction_year(Aggre_insu, year)
            
            Quarter = st.selectbox("Select the Quarter", Tran_year["Quarter"].unique())
            Transaction_Quarter(Tran_year, Quarter)
        
        elif show_trn_analysis == "Aggregate_Transaction_Analysis":
            year = st.selectbox("Select the Year", Aggre_trns["Years"].unique())
            Tran_year = Transaction_year(Aggre_trns, year)
            
            states = st.selectbox("Select the State", Aggre_trns["States"].unique())
            Transaction_type(Tran_year, states)
            
            Quarter = st.selectbox("Select the Quarter", Tran_year["Quarter"].unique())
            Transaction_Quarter(Tran_year, Quarter)
        
        elif show_trn_analysis == "Aggregate_User_Analysis":
            Brands = st.selectbox("Select the Brands", Aggre_users["Years"].unique())
            user_brands = user_brand(Aggre_users, Brands)
            
            Quarter = st.selectbox("Select the Quarter", user_brands["Quarter"].unique())
            user_quarter(user_brands, Quarter)
            
            states = st.selectbox("Select the State", Aggre_users["States"].unique())
            user_state(Aggre_users, states)

    with st.expander("Map Analysis"):
        show_map_analysis = st.radio("Select the Analysis", ["Map_Insurance_Analysis", "Map_Transaction_Analysis", "Map_User_Analysis"])
        st.write("Your selected analysis:", show_map_analysis)
        
        if show_map_analysis == "Map_Insurance_Analysis":
            map_years = st.selectbox("Select the years", map_insu["Years"].unique())
            Tran_year = Transaction_year(map_insu, map_years)
            states = st.selectbox("Select the states", Tran_year["States"].unique())
            District_type(Tran_year, states)
            map_Quarters = st.selectbox("Select the quarters", Tran_year["Quarter"].unique())
            Transaction_Quarter(Tran_year, map_Quarters)

        elif show_map_analysis == "Map_Transaction_Analysis":
            map_years = st.selectbox("Select the Years", map_trns["Years"].unique())
            Tran_year = Transaction_year(map_trns, map_years)
            states = st.selectbox("Select the States", Tran_year["States"].unique())
            District_type(Tran_year, states)
            Quarter = st.selectbox("Select the Quarters", Tran_year["Quarter"].unique())
            Transaction_Quarter(Tran_year, Quarter)

        elif show_map_analysis == "Map_User_Analysis":
            users = st.selectbox("Select the yrs", map_users["Years"].unique())
            user_brands = state_sale(map_users, users)
            
            Quarter = st.selectbox("Select the Qrtrs", map_users["Quarter"].unique())
            Quarter_user(map_users, Quarter)

    with st.expander("Top Analysis"):
        show_top_analysis = st.radio("Select the Analysis", ["Top_Insurance_Analysis", "Top_Transaction_Analysis", "Top_User_Analysis"])
        st.write("Your selected analysis:", show_top_analysis)
        
        if show_top_analysis == "Top_Insurance_Analysis":
            map_years = st.selectbox("Select the yrs", top_insu["Years"].unique())
            Tran_year = Transaction_year(top_insu, map_years)
            map_Quarters = st.selectbox("Select the qurtrs", Tran_year["Quarter"].unique())
            Transaction_Quarter(Tran_year, map_Quarters)           
            
        elif show_top_analysis == "Top_Transaction_Analysis":
            year = st.selectbox("Select the yEARS", top_trns["Years"].unique())
            Tran_year = Transaction_year(Aggre_trns, year)
            
            states = st.selectbox("Select the STATES", top_trns["States"].unique())
            Transaction_type(Tran_year, states)
            
            Quarter = st.selectbox("Select the QUARTERS", Tran_year["Quarter"].unique())
            Transaction_Quarter(Tran_year, Quarter)
            
        
        elif show_top_analysis == "Top_User_Analysis":
            year = st.selectbox("Select the yEARS", top_users["Years"].unique())
            Tran_year = Transaction_year(top_trns, year)
            
            Quarter = st.selectbox("Select the QUARTERS", Tran_year["Quarter"].unique())
            Transaction_Quarter(Tran_year, Quarter)
            

            

         

        

