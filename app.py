#  Importing Important library
import streamlit as st
import dbhelper as dbo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

db=dbo.DataBase()
#  Adding title to dashboard
st.sidebar.title("Flight dashboard of India")
# Provide dropdown menu to user in the form of list
user_option = st.sidebar.selectbox("menu",["select one","check flight","analytics"])
if user_option=="check flight":
    st.title("Check Flights")
    col1,col2=st.columns(2)
    # Get unique cities in dropdown from dbhelper file
    response = db.unique_city()
    with col1:
        source=st.selectbox("Source",response)
    with col2:
        destination = st.selectbox("destination",response)
    # Adding button with Search Flight as label
    button=st.button(label="Search Flight")

    try:
        if button:
            # With dbhelper file get the required data
            data = db.source_destination_flight(source, destination)
            df=pd.DataFrame(data,columns=["Airline","Date of Journey","Source","Destination","Route","Dep_time","Duration","Total_stops","Price"])
            if len(df)==0:
                st.title(f"No direct flight between {source} to {destination}")
            else:
                st.dataframe(df)
                st.write(f"Airlines and total number of flight between {source} to {destination}")
                col3,col4=st.columns(2)
                with col3:
                    flight_counts = db.airline_value_counts(source, destination)
                    flight_dataframe = pd.DataFrame(flight_counts, columns=["Airline", "Number_Of_Flights"])
                    st.dataframe(flight_dataframe)
                with col4:
                    fig, ax = plt.subplots()
                    ax.pie(flight_dataframe.Number_Of_Flights,labels=flight_dataframe.Airline, autopct='%1.1f%%', startangle=140)
                    ax.axis("Equal")
                    st.pyplot(fig)
                st.write(f"Average price for non-stop {source} to {destination} flight for each airline")
                col5,col6=st.columns(2)
                with col5:
                    airline_price=db.airline_price_non_stop(source,destination)
                    airline_price_df=pd.DataFrame(airline_price,columns=["Airline","Average Price"])
                    st.dataframe(airline_price_df)
                with col6:
                    plt.figure(figsize=(8, 6))
                    sns.barplot(x='Airline', y='Average Price', data=airline_price_df)
                    plt.title('Average price for each Airline')
                    plt.xticks(rotation=90)
                    st.pyplot(plt)





    except:
        st.title(f"No flight between {source} and {destination}")

elif user_option == "analytics":
    # With dbhelper file get the required data
    st.title("Airline Statistics")
    airline_details=db.stat_by_airline()
    airline_details_df=pd.DataFrame(airline_details,columns=["Airline","Average Fare","Number Of flights Fly till date","Average Time of fly","Total revenue"])
    st.dataframe(airline_details_df)
    col7,col8=st.columns(2)
    with col7:
        st.write("Frequency of flight top 5 airline")
        airline_count=db.top_5_airline_with_high_freq()
        airline_count_df=pd.DataFrame(airline_count,columns=['airline','Frequency_of_flight'])
        fig, ax = plt.subplots()
        ax.pie(airline_count_df.Frequency_of_flight, labels=airline_count_df.airline, autopct='%1.1f%%', startangle=140)
        ax.axis("Equal")
        st.pyplot(fig)
    with col8:
        st.write("Average Fare of flight per airline")
        airline_fare=db.top_5_airline_with_high_ave_fare()
        airline_fare_df=pd.DataFrame(airline_fare,columns=["airline","Average_Fare"])
        plt.figure(figsize=(8, 6))
        sns.barplot(x='airline', y='Average_Fare', data=airline_fare_df)
        plt.title('Average price for top 5 Airline')
        plt.xticks(rotation=90)
        st.pyplot(plt)

    st.write("Total revenue per airline")
    airline_revenue = db.top_5_airline_with_highest_revenue()
    airline_revenue_df = pd.DataFrame(airline_revenue, columns=["airline", "total_revenue"])
    plt.figure(figsize=(8, 3))
    sns.barplot(x='airline', y='total_revenue', data=airline_revenue_df)
    plt.title('Total Revenue of top 5 Airline')
    plt.xticks(rotation=90)
    st.pyplot(plt)
    col9,col10=st.columns(2)
    with col9:
        st.write("Top 5 Busiest Airport")
        busy_airport=db.top_5_busy_airport()
        busy_airport_df=pd.DataFrame(busy_airport,columns=["Airport","total flight takeoff and landed"])
        st.dataframe(busy_airport_df)
    with col10:
        st.write("Top 5 Busiest Airport")
        fig, ax = plt.subplots()
        ax.pie(busy_airport_df["total flight takeoff and landed"], labels=busy_airport_df.Airport, autopct='%1.1f%%', startangle=140)
        ax.axis("Equal")
        st.pyplot(fig)
    air=db.unique_airlines()
    selected_airline=st.selectbox("Select Airline",air)
    button_1=st.button(label="Analysis")
    if button_1:
        air_info=db.average_fare_per_airline(selected_airline)
        airline_info_df=pd.DataFrame(air_info).T
        airline_info_df.index=['Minimum Fare','Maximum Fare','Average Fare','Average duration In Minutes']
        airline_info_df.columns=['Values']
        st.dataframe(airline_info_df)



