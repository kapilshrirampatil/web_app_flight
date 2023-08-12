# importing library to interact with database
import mysql.connector

class DataBase:
    def __init__(self):
        # connect to database
        try:
            self.connection = mysql.connector.connect(
                                                host="127.0.0.1",
                                                user="root",
                                                password="Kapil1396",
                                                database="flight_air")
            self.mycursor = self.connection.cursor()
            print("connection successful")
        except:
            print("connection failed")
    # find out unique cities from data.
    def unique_city(self):
        self.mycursor.execute('''SELECT DISTINCT Source FROM flights 
                                 UNION 
                                 SELECT DISTINCT Destination FROM flights''')
        data=self.mycursor.fetchall()
        city_list=[]
        for i in data:
            city_list.append(i[0])
        return city_list
    # fetch all the data between source and destination.
    def source_destination_flight(self,source,destination):

        self.mycursor.execute("""
        SELECT * from flights 
        where Source = '{}' and Destination = '{}'""".format(source,destination))
        data = self.mycursor.fetchall()
        return data
    # total number of flights per airline between souce city and destination city
    def airline_value_counts(self,source,destination):
        self.mycursor.execute(f"""
        SELECT Airline,Count(*) FROM flights 
        WHERE source='{source}' and destination='{destination}'
        GROUP BY Airline ORDER BY COUNT(*) desc """)
        data=self.mycursor.fetchall()
        return data
    #  for non-stop flight average price for each airline
    def airline_price_non_stop(self,source,destination):
        self.mycursor.execute(f"""
        SELECT airline,ROUND(AVG(price),2) FROM flights
        WHERE Source='{source}' and Destination='{destination}' and Total_Stops='non-stop' 
        GROUP BY airline ORDER BY AVG(price) DESC""")
        data=self.mycursor.fetchall()
        return data
    # fetch all the unique airline from data
    def unique_airlines(self):
        self.mycursor.execute("""
        SELECT DISTINCT Airline FROM flights""")
        airlines=self.mycursor.fetchall()
        unique_airline=[]
        for i in airlines:
            unique_airline.append(i[0])
        return unique_airline
    #  calculating min,max,avg,price and avg duration for a particular airline
    def average_fare_per_airline(self,airline):
        self.mycursor.execute("""
        SELECT ROUND(MIN(price),2),Round(MAX(PRICE),2),ROUND(AVG(PRICE),2),ROUND(AVG(duration),2) FROM flights WHERE airline='{}'""".format(airline))
        data=self.mycursor.fetchall()
        return data
    # general stat per airline
    def stat_by_airline(self):
        self.mycursor.execute("""SELECT airline,ROUND(AVG(price),2),COUNT(*),ROUND(AVG(DURATION),2),ROUND(sum(price),2)
         FROM flights GROUP BY airline order by airline asc""")
        data=self.mycursor.fetchall()
        return data
    #  finding top 5 airline with highest number of flight
    def top_5_airline_with_high_freq(self):
        self.mycursor.execute("""SELECT airline,COUNT(*) FROM flights GROUP BY airline order by count(*) DESC limit 5""")
        data=self.mycursor.fetchall()
        return data
    #  finding top 5 airline with highest average fare
    def top_5_airline_with_high_ave_fare(self):
        self.mycursor.execute("""SELECT airline,ROUND(AVG(price),2) 
        FROM flights GROUP BY airline order by ROUND(AVG(price),2) DESC limit 5""")
        data = self.mycursor.fetchall()
        return data

    #  finding top 5 airline with highest revenue
    def top_5_airline_with_highest_revenue(self):
        self.mycursor.execute("""SELECT airline,ROUND(SUM(price),2) 
        FROM flights GROUP BY airline order by ROUND(SUM(price),2) DESC limit 5""")
        data = self.mycursor.fetchall()
        return data

    #  finding top 5 busiest airport on the basis of most number of flight take of and land
    def top_5_busy_airport(self):
        self.mycursor.execute("""with table_1 as 
        (SELECT Source,count(*) as "source count" from flights group by source
        union SELECT Destination,count(*) as "Destination count" from flights group by destination)
        select source,sum(`source count`) as "flights_takeoff" from table_1 group by source order by flights_takeoff desc limit 5""")
        data=self.mycursor.fetchall()
        return data



