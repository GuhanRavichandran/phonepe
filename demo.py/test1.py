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

import pandas as pd
import requests as rq
import json
import plotly.express as px
import streamlit as st

def Transaction_year(df, year):   
    # Filter data for the specified year
    Table_year = df[df["Years"] == year].copy()
    Table_year.reset_index(drop=True, inplace=True)

    # Aggregate transaction count and amount by states
    Table_group = Table_year.groupby("States")[["Transaction_count", "Transaction_amount"]].sum().reset_index()

    # Load India states geojson data
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = rq.get(url)
    data = json.loads(response.content)

    # Create layout using Streamlit st.columns
    column1, column2 = st.columns(2)

    with column1:
        # Plot bar chart for Transaction Amount
        fig_amount = px.bar(Table_group, x="States", y="Transaction_amount",
                            title=f"Transaction Amount {year}",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount)

        # Plot choropleth map for Transaction Amount
        fig_india = px.choropleth(Table_group,
                                  geojson=data,
                                  locations="States",
                                  featureidkey="properties.ST_NM",
                                  color="Transaction_amount",
                                  color_continuous_scale="turbid",
                                  range_color=(Table_group["Transaction_amount"].min(), Table_group["Transaction_amount"].max()),
                                  hover_name="States",
                                  title=f"Transaction Amount {year}",
                                  fitbounds="locations",
                                  height=400,  # Adjust height as needed
                                  width=500    # Adjust width as needed
                                 )
        fig_india.update_geos(
            visible=False,  # Hide the default world map
            lonaxis=dict(range=[60, 100]),  # Longitude range for India
            lataxis=dict(range=[5, 40])     # Latitude range for India
        )
        st.plotly_chart(fig_india)

    with column2:
        # Plot bar chart for Transaction Count
        fig_count = px.bar(Table_group, x="States", y="Transaction_count",
                           title=f"Transaction Count {year}",
                           color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_count)

        # Plot choropleth map for Transaction Count
        fig_india1 = px.choropleth(Table_group,
                                   geojson=data,
                                   locations="States",
                                   featureidkey="properties.ST_NM",
                                   color="Transaction_count",
                                   color_continuous_scale="ylorbr",
                                   range_color=(Table_group["Transaction_count"].min(), Table_group["Transaction_count"].max()),
                                   hover_name="States",
                                   title=f"Transaction Count {year}",
                                   fitbounds="locations",
                                   height=400,  # Adjust height as needed
                                   width=400    # Adjust width as needed
                                  )
        fig_india1.update_geos(
            visible=False,  # Hide the default world map
            lonaxis=dict(range=[60, 100]),  # Longitude range for India
            lataxis=dict(range=[5, 40])     # Latitude range for India
        )
        st.plotly_chart(fig_india1)

    return Table_year

     
def Transaction_Quarter(df, Quarter):
    Table_Quarter = df[df["Quarter"] == Quarter]
    Table_Quarter.reset_index(drop=True, inplace=True)

    Table_group = Table_Quarter.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    Table_group.reset_index(inplace=True)
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = rq.get(url)
    data = json.loads(response.content)
    
    column1, column2 = st.columns(2)
    
    with column1:
        fig_amount = px.bar(Table_group, x="States", y="Transaction_amount",
                            title=f"{Table_Quarter['Years'].max()} Transaction Amount in Qtr {Quarter}",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(fig_amount)
            
        fig_india = px.choropleth(Table_group, 
                                  geojson=data, 
                                  locations="States", 
                                  featureidkey="properties.ST_NM",
                                  color="Transaction_amount", 
                                  color_continuous_scale="turbid",
                                  range_color=(Table_group["Transaction_amount"].min(), Table_group["Transaction_amount"].max()),
                                  hover_name="States", 
                                  title=f"{Table_Quarter['Years'].max()} Transaction Amount in Qtr {Quarter}",
                                  fitbounds="locations",
                                  height=400,  # Adjust height as needed
                                  width=400    # Adjust width as needed
                                 )
        fig_india.update_geos(
            visible=False,  # Hide the default world map
            lonaxis=dict(range=[60, 100]),  # Longitude range for India
            lataxis=dict(range=[5, 40])     # Latitude range for India
        )

        st.plotly_chart(fig_india)
    
    with column2:
        fig_count = px.bar(Table_group, x="States", y="Transaction_count",
                           title=f"{Table_Quarter['Years'].max()} Transaction Count in Qtr {Quarter}",
                           color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_count)
        
        fig_india1 = px.choropleth(Table_group, 
                                   geojson=data, 
                                   locations="States", 
                                   featureidkey="properties.ST_NM",
                                   color="Transaction_count", 
                                   color_continuous_scale="ylorbr",
                                   range_color=(Table_group["Transaction_count"].min(), Table_group["Transaction_count"].max()),
                                   hover_name="States", 
                                   title=f"{Table_Quarter['Years'].max()} Transaction Count in Qtr {Quarter}",
                                   fitbounds="locations",
                                   height=400,  # Adjust height as needed
                                   width=400    # Adjust width as needed
                                  )
        fig_india1.update_geos(
            visible=False,  # Hide the default world map
            lonaxis=dict(range=[60, 100]),  # Longitude range for India
            lataxis=dict(range=[5, 40])     # Latitude range for India
        )

        st.plotly_chart(fig_india1)

    return Table_Quarter

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
    
def Top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)

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
analysis_options = st.radio("Select the Options", ("PHONEPE_VISUALISATION","PHONEPE_ANALYSIS","DATA_EXPLORATION",
                                                  "EXPLORATED_FINDING" ))

if analysis_options=="PHONEPE_VISUALISATION":
    col1,col2= st.columns(2)
    
    with col1:    
     st.image(r"C:\Users\Hp\OneDrive\Desktop\demo.py\image_processing20200114-26356-1dzvejl - Copy.gif", use_column_width=True)
    st.subheader(
            "PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
    st.markdown("[DOWNLOAD APP](https://www.phonepe.com/app-download/)")

    with col2:
           st.video("C:\\Users\\Hp\\OneDrive\\Desktop\\demo.py\\Introducing PhonePe Pulse.mp4")


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
        st.image(r"C:\Users\Hp\OneDrive\Desktop\demo.py\phonepe.jpeg", use_column_width=True)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(r"C:\Users\Hp\OneDrive\Desktop\demo.py\phonepe2.jpeg", use_column_width=True)
              
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
    
    with col6:
        st.image(r"C:\Users\Hp\OneDrive\Desktop\demo.py\phonepe3.jpeg", use_column_width=True)


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
            year = st.selectbox("Select the YEARS", top_trns["Years"].unique())
            Top_year = Transaction_year(top_trns, year)
            
            states = st.selectbox("Select the STATES", top_trns["States"].unique())
            Top_insurance_plot_1(top_trns, states)
            
            Quarter = st.selectbox("Select the QUARTERS", Top_year["Quarter"].unique())
            Transaction_Quarter(Top_year, Quarter)
            
        
        elif show_top_analysis == "Top_User_Analysis":
            year = st.selectbox("Select the yEARS", top_users["Years"].unique())
            Tran_year = Transaction_year(top_trns, year)
            
            Quarter = st.selectbox("Select the QUARTERS", Tran_year["Quarter"].unique())
            Transaction_Quarter(Tran_year, Quarter)
            
    
if analysis_options=="EXPLORATED_FINDING":
    Analysis_ques=st.selectbox("Select the Question",("Top Transaction types based on the Transaction Amount",
                                "Top Brands Of Mobiles Used",
                                "Top 10 states based on year and amount of transaction",
                                "Least 10 states based on year and amount of transaction",
                                "Top 10 States and Districts based on Registered Users",
                                "Least 10 States and Districts based on Registered Users",
                                "Top 10 Districts based on the Transaction Amount",
                                "Least 10 Districts based on the Transaction Amount",
                                "Top 10 Districts based on the Transaction count",
                                "Least 10 Districts based on the Transaction count",
                                ))
    
    if Analysis_ques=="Top Transaction types based on the Transaction Amount":
        mycursor.execute("SELECT DISTINCT Transaction_type, SUM(Transaction_amount) AS Amount FROM aggregate_transaction GROUP BY Transaction_type ORDER BY Amount DESC LIMIT 5") 
        columndata=mycursor.fetchall() 
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_bar=px.bar(df,x="Transaction_type",y="Amount",title=f"Top Transaction_type")
        st.plotly_chart(fig_bar)
    
    if Analysis_ques=='Top Brands Of Mobiles Used':
        mycursor.execute("SELECT Brands, COUNT(*) AS BrandCount FROM aggregate_user GROUP BY Brands ORDER BY BrandCount DESC LIMIT 10;")
        columndata=mycursor.fetchall()
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_line=px.line(df, x="Brands",y="BrandCount",title=f"Top Brands")
        st.plotly_chart(fig_line)
    
    if Analysis_ques=="Top 10 states based on year and amount of transaction":
        mycursor.execute("SELECT distinct States, SUM(Transaction_amount) AS TotalTransactionAmount, Years FROM aggregate_transaction GROUP BY States, Years ORDER BY TotalTransactionAmount DESC LIMIT 10;")
        columndata=mycursor.fetchall()                                                                                     
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_pie=px.pie(data_frame=df, names="States",values="TotalTransactionAmount",width=600,title=f"Top states")
        fig_pie.update_traces(textinfo="label+value")
        st.plotly_chart(fig_pie)
        
    if Analysis_ques=="Least 10 states based on year and amount of transaction":
        mycursor.execute("SELECT distinct States, SUM(Transaction_amount) AS TotalTransactionAmount, Years FROM aggregate_transaction GROUP BY States, Years ORDER BY TotalTransactionAmount ASc LIMIT 10;")
        columndata=mycursor.fetchall()                                                                                     
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_pie=px.pie(data_frame=df, names="States",values="TotalTransactionAmount",width=600,title=f"Least states")
        fig_pie.update_traces(textinfo="label+value")
        st.plotly_chart(fig_pie)
        
    if Analysis_ques=="Top 10 States and Districts based on Registered Users":
        mycursor.execute("SELECT DISTINCT States,Pincodes, SUM(Registered_Users) AS Users FROM top_user GROUP BY States,Pincodes ORDER BY Users DESC LIMIT 10")
        columndata=mycursor.fetchall() 
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_bar=px.bar(df,x="Users",y="States",title=f"Top Registeredusers")
        st.plotly_chart(fig_bar)
        
    if Analysis_ques=="Least 10 States and Districts based on Registered Users":
        mycursor.execute("SELECT DISTINCT States,Pincodes, SUM(Registered_Users) AS Users FROM top_user GROUP BY States,Pincodes ORDER BY Users ASC LIMIT 10")
        columndata=mycursor.fetchall() 
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_bar=px.bar(df,x="Users",y="States",title=f"Least Registeredusers")
        st.plotly_chart(fig_bar)
        
    if Analysis_ques=="Top 10 Districts based on the Transaction Amount":
        mycursor.execute("SELECT DISTINCT States ,Districts,SUM(Transaction_amount) AS Transactions FROM map_transaction GROUP BY States ,Districts ORDER BY Transactions DESC LIMIT 10") 
        columndata=mycursor.fetchall() 
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_bar=px.bar(df,x="Districts",y="Transactions",title=f"Top Transaction in districts")
        st.plotly_chart(fig_bar)     
        
    if Analysis_ques=="Least 10 Districts based on the Transaction Amount":
        mycursor.execute("SELECT DISTINCT States ,Districts,SUM(Transaction_amount) AS Transactions FROM map_transaction GROUP BY States ,Districts ORDER BY Transactions ASC LIMIT 10") 
        columndata=mycursor.fetchall() 
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_bar=px.bar(df,x="Districts",y="Transactions",title=f"Least Transaction in districts")
        st.plotly_chart(fig_bar)
        
    if Analysis_ques=="Top 10 Districts based on the Transaction count":
        mycursor.execute("SELECT DISTINCT States ,Districts,SUM(Transaction_count) AS counts FROM map_transaction GROUP BY States ,Districts ORDER BY counts DESC LIMIT 10") 
        columndata=mycursor.fetchall() 
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_bar=px.bar(df,x="Districts",y="counts",title=f"Top Transaction_count in districts")
        st.plotly_chart(fig_bar)  
        
    if Analysis_ques=="Least 10 Districts based on the Transaction count":
        mycursor.execute("SELECT DISTINCT States ,Districts,SUM(Transaction_count) AS counts FROM map_transaction GROUP BY States ,Districts ORDER BY counts ASC LIMIT 10") 
        columndata=mycursor.fetchall() 
        df=pd.DataFrame(columndata,columns=mycursor.column_names)
        fig_bar=px.bar(df,x="Districts",y="counts",title=f"Least Transaction_count in districts")
        st.plotly_chart(fig_bar) 
        
   


     

    

     

            

         

        

