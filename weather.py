import requests
from datetime import datetime, timezone
from sys import argv

API_KEY = '8d23c782004b031820da6026ceeb130f' 

def get_weather(city):
    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en")
        r.raise_for_status()
        info = r.json()
        if r.status_code==200:
            tempr=info["main"]["temp"]
            humidity = info["main"]["humidity"]
            description = info["weather"][0]["description"]
            country = info["sys"]["country"]
            sunrise = datetime.fromtimestamp(info["sys"]["sunrise"],tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            sunset  = datetime.fromtimestamp(info["sys"]["sunset"],tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                "tempr": tempr,
                "description":description,
                "humidity":humidity,
                "country":country,
                "sunset":sunset,
                "sunrise":sunrise
            }
    except requests.exceptions.RequestException:
        print("Network error! Please check your internet connection.")
    except requests.exceptions.HTTPError:
        print("City not found. check your spelling and try again")
    except KeyError:
        print("Could not fetch deatils try again later")
    

# def main():
#     if len(argv)!=2:
#         print(f"ERROR! Usage: {argv[0]} CITY_NAME")
#         exit(1)
#     city=argv[1].strip()
#     if city.lower() == 'exit':
#         print("Thank you for using our WEATHER APP")
#         exit(1)
#     elif city=='':
#         print("ERROR! city name cannot be empty!")
#     else:
#         get_weather(city)

# main()