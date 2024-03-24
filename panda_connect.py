import sqlconnect as sq
import pandas as pd
import numpy as np

sq.mycursor.execute("select*from chennai_weather")

df_chennai=pd.DataFrame(sq.mycursor.fetchall(),columns=['id','_date_','temprature','apparent_temprature','surface_pressure','humidity','windspead','precipitation','day'])
#print(df_chennai)

sq.mycursor.execute("select*from madurai_weather")
df_madurai=pd.DataFrame(sq.mycursor.fetchall(),columns=['id','_date_','temprature','apparent_temprature','surface_pressure','humidity','windspead','precipitation','day'])
#print(df_madurai)

#testing
#plt.plot(df_chennai['id'],df_chennai['temprature'])
#plt.show()

#array temperature of cities
array_chennai_temp=np.array(df_chennai['temprature'],dtype=np.float32)
array_madurai_temp=np.array(df_madurai['temprature'],dtype=np.float32)

#array apparent temprature of cities
array_chennai_app_temp=np.array(df_chennai['apparent_temprature'],dtype=np.float32)
array_madurai_app_temp=np.array(df_madurai['apparent_temprature'],dtype=np.float32)

#array humidity of cities
array_chennai_humidity=np.array(df_chennai['humidity'],dtype=np.float32)
array_madurai_humidity=np.array(df_madurai['humidity'],dtype=np.float32)

#array surafce pressure of cities
array_chennai_surfacepress=np.array(df_chennai['surface_pressure'],dtype=np.float32)
array_madurai_surfacepress=np.array(df_madurai['surface_pressure'],dtype=np.float32)

#array windspeed of cities
array_chennai_windspeed=np.array(df_chennai['windspead'],dtype=np.float32)
array_madurai_windspeed=np.array(df_madurai['windspead'],dtype=np.float32)

#array precipitation of cities
array_chennai_precipitation=np.array(df_chennai['precipitation'],dtype=np.float32)
array_madurai_precipiattion=np.array(df_madurai['precipitation'],dtype=np.float32)


class stat:
    
    def __init__(self,arr_city):
        self.arr_city=arr_city
    
    def mean_derive(self):
        return round(np.mean(self.arr_city),3)
    
    def std_derive(self):
        return round(np.std(self.arr_city),3)
    
    def median_derive(self):
        return round(np.median(self.arr_city),3)
    
    def var_derive(self):
        return round(np.var(self.arr_city),3)

chen_temp=stat(array_chennai_temp)
chen_temp_stat=[chen_temp.mean_derive(),chen_temp.median_derive(),chen_temp.std_derive()]
mad_temp=stat(array_madurai_temp)
mad_temp_stat=[mad_temp.mean_derive(),mad_temp.median_derive(),mad_temp.std_derive()]

chen_app_temp=stat(array_chennai_app_temp)
chen_apptemp_stat=[chen_app_temp.mean_derive(),chen_app_temp.median_derive(),chen_app_temp.std_derive()]
mad_app_temp=stat(array_madurai_app_temp)
mad_apptemp_stat=[mad_app_temp.mean_derive(),mad_app_temp.median_derive(),mad_app_temp.std_derive()]

chen_humid=stat(array_chennai_humidity)
chen_humid_stat=[chen_humid.mean_derive(),chen_humid.median_derive(),chen_humid.std_derive()]
mad_humid=stat(array_madurai_humidity)
mad_humid_stat=[mad_humid.mean_derive(),mad_humid.median_derive(),mad_humid.std_derive()]

chen_precip=stat(array_chennai_precipitation)
chen_precip_stat=[chen_precip.mean_derive(),chen_precip.median_derive(),chen_precip.std_derive()]
mad_precip=stat(array_madurai_precipiattion)
mad_precip_stat=[mad_precip.mean_derive(),mad_precip.median_derive(),mad_precip.std_derive()]

chen_surf=stat(array_chennai_surfacepress)
chen_surf_stat=[chen_surf.mean_derive(),chen_surf.median_derive(),chen_surf.std_derive()]
mad_surf=stat(array_madurai_surfacepress)
mad_surf_stat=[mad_surf.mean_derive(),mad_surf.median_derive(),mad_surf.std_derive()]

chen_wind=stat(array_chennai_windspeed)
chen_wind_stat=[chen_wind.mean_derive(),chen_wind.median_derive(),chen_wind.std_derive()]
mad_wind=stat(array_madurai_windspeed)
mad_wind_stat=[mad_wind.mean_derive(),mad_wind.median_derive(),mad_wind.std_derive()]

def mean_table():
    str_mean="insert into mean_table(city,temprature,apparent_temprature,surface_pressure,humidity,windspead,precipitation) values('chennai',{},{},{},{},{},{})".format(chen_temp_stat[0],chen_apptemp_stat[0],chen_surf_stat[0],chen_humid_stat[0],chen_wind_stat[0],chen_precip_stat[0])
    sq.mycursor.execute(str_mean)
    sq.mydb.commit()
    str_mean2="insert into mean_table(city,temprature,apparent_temprature,surface_pressure,humidity,windspead,precipitation) values('madurai',{},{},{},{},{},{})".format(mad_temp_stat[0],mad_apptemp_stat[0],mad_surf_stat[0],mad_humid_stat[0],mad_wind_stat[0],mad_precip_stat[0])
    sq.mycursor.execute(str_mean2)
    sq.mydb.commit()
#mean_table()
def median_table():
    str_median="insert into median_table(city,temprature,apparent_temprature,surface_pressure,humidity,windspead,precipitation) values('chennai',{},{},{},{},{},{})".format(chen_temp_stat[1],chen_apptemp_stat[1],chen_surf_stat[1],chen_humid_stat[1],chen_wind_stat[1],chen_precip_stat[1])
    str_median2="insert into median_table(city,temprature,apparent_temprature,surface_pressure,humidity,windspead,precipitation) values('madurai',{},{},{},{},{},{})".format(mad_temp_stat[1],mad_apptemp_stat[1],mad_surf_stat[1],mad_humid_stat[1],mad_wind_stat[1],mad_precip_stat[1])
    sq.mycursor.execute(str_median)
    sq.mydb.commit()
    sq.mycursor.execute(str_median2)
    sq.mydb.commit()
median_table()
def std_table():
    str_std="insert into standard_diviation_table(city,temprature,apparent_temprature,surface_pressure,humidity,windspead,precipitation) values('chennai',{},{},{},{},{},{})".format(chen_temp_stat[2],chen_apptemp_stat[2],chen_surf_stat[2],chen_humid_stat[2],chen_wind_stat[2],chen_precip_stat[2])
    str_std2="insert into standard_diviation_table(city,temprature,apparent_temprature,surface_pressure,humidity,windspead,precipitation) values('madurai',{},{},{},{},{},{})".format(mad_temp_stat[2],mad_apptemp_stat[2],mad_surf_stat[2],mad_humid_stat[2],mad_wind_stat[2],mad_precip_stat[2])
    sq.mycursor.execute(str_std)
    sq.mydb.commit()
    sq.mycursor.execute(str_std2)
    sq.mydb.commit()
std_table()
