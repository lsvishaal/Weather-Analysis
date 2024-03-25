import mysql.connector

mydb = mysql.connector.connect(host="localhost",user="root",password="root", database="weather_db")
# print(mydb) sucessful

mycursor=mydb.cursor()

#mycursor.execute("create database if not exists weather_db")
#mycursor.execute("show databases")

# for a in mycursor:
#     print(a)
mycursor.execute("create table if not exists chennai_weather(id int auto_increment primary key,_date_ datetime default now(),temprature float, apparent_temprature float, surface_pressure float, humidity float, windspead float, precipitation float, day bool)")
mycursor.execute("desc chennai_weather")
for a in mycursor:
     print(a)
#mycursor.execute("create table if not exists mumbai_weather(id int auto_increment primary key,_date_ date, _time_ time, temprature float, min_temprature float, max_temprature float, pressure float, humidity float, windspead float, precipitation float, description varchar(80))")
#succesfully created the databse and created two tables for both chennai and mumbai
mycursor.execute("create table if not exists madurai_weather(id int auto_increment primary key,_date_ datetime default now(),temprature float, apparent_temprature float, surface_pressure float, humidity float, windspead float, precipitation float, day bool)")


mycursor.execute("create table if not exists mean_table(id int auto_increment primary key,_date_ datetime default now(),city varchar(15),temprature float, apparent_temprature float, surface_pressure float, humidity float, windspead float, precipitation float)")
mycursor.execute("create table if not exists median_table(id int auto_increment primary key,_date_ datetime default now(),city varchar(15),temprature float, apparent_temprature float, surface_pressure float, humidity float, windspead float, precipitation float)")
mycursor.execute("create table if not exists standard_diviation_table(id int auto_increment primary key,_date_ datetime default now(),city varchar(15),temprature float, apparent_temprature float, surface_pressure float, humidity float, windspead float, precipitation float)")
