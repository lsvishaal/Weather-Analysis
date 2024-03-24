import requests
import json
import sqlconnect as mq
#madurai
#api url
url1="https://api.open-meteo.com/v1/forecast?latitude=9.919&longitude=78.1195&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,cloud_cover,surface_pressure,wind_speed_10m,wind_direction_10m"
response1 = requests.get(url1)

# Print the response
#print(response.content.decode())
x1=json.dumps(response1.json(),indent=2)
y1=json.loads(x1)
print(x1)
#print(y.keys())
current_values1=y1['current']
# print(current_values['temperature_2m'])
# j="insert into chennai_weather(temprature) values({})".format(current_values['temperature_2m'])
# mq.mycursor.execute(j)
# mq.mydb.commit()

#chennai

url2="https://api.open-meteo.com/v1/forecast?latitude=13.0878&longitude=80.2785&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,cloud_cover,surface_pressure,wind_speed_10m,wind_direction_10m"

response2=requests.get(url2)

x2=json.dumps(response2.json(),indent=2)
y2=json.loads(x2)
print(x2)
current_values2=y2['current']

#functions to insert the values from the api to the database

def madurai_values(dict_values=current_values1):
    str1="insert into madurai_weather(temprature,apparent_temprature,surface_pressure,humidity,windspead,precipitation,day) values({},{},{},{},{},{},{})".format(current_values1['temperature_2m'],current_values1['apparent_temperature'],current_values1['surface_pressure'],current_values1['relative_humidity_2m'],current_values1['wind_speed_10m'],current_values1['precipitation'],current_values1['is_day'])
    mq.mycursor.execute(str1)
    mq.mydb.commit()
madurai_values()
def chennai_values(dict_values=current_values2):
    str1="insert into chennai_weather(temprature,apparent_temprature,surface_pressure,humidity,windspead,precipitation,day) values({},{},{},{},{},{},{})".format(current_values2['temperature_2m'],current_values2['apparent_temperature'],current_values2['surface_pressure'],current_values2['relative_humidity_2m'],current_values2['wind_speed_10m'],current_values2['precipitation'],current_values2['is_day'])
    mq.mycursor.execute(str1)
    mq.mydb.commit()
#chennai_values()
    





