import requests
import json
from datetime import datetime
import pytz


class WeatherService:

    key = 'c47c0aa3ca0e3de709cc921a6f485819'

    def __init__(self):
        self.timezone = pytz.timezone('UTC')

    @staticmethod
    def kelvin_to_c(temp):
        return temp - 273


    @staticmethod
    def get_str_from_timestamp(ts):
        dt = datetime.fromtimestamp(ts)
        if 22 < dt.hour or dt.hour < 4:
            return 'night'
        elif 11 > dt.hour > 4 or 23 > dt.hour > 16:
            return 'evening-morning'
        elif 11 < dt.hour < 17:
            return 'day'

    @staticmethod
    def get_time_at_destination(timezone):
        tt = datetime.timestamp(datetime.utcnow()) + timezone
        return tt

    @staticmethod
    def generate_real_time(tt):
        hour = datetime.fromtimestamp(tt).hour
        minute = datetime.fromtimestamp(tt).minute
        if hour < 10:
            real_hour = f'0{hour}'
        else:
            real_hour = str(hour)
        if minute < 10:
            real_minute = f'0{minute}'
        else:
            real_minute = str(minute)
        return f'{real_hour}:{real_minute}'

    def get_data_by_city(self, city):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.key}'
        response = requests.get(url).text
        weather_data = json.loads(response)
        return weather_data

    def get_gata_dict(self, city):
        crude_data = self.get_data_by_city(city)
        if 'message' in crude_data.keys():
            return 'Wrong city name!'
        else:
            state = crude_data.get('weather')[0].get('main')
            degrees = round(self.kelvin_to_c(crude_data.get('main').get('temp')))
            timezone = crude_data.get('timezone')
            tt = self.get_time_at_destination(timezone)
            time = self.get_str_from_timestamp(tt)
            th = self.generate_real_time(tt)
            return {'city': city, 'state': state, 'degrees': degrees, 'time': time, 'th': th}


lel = WeatherService()
kek = lel.get_data_by_city('Tallinn')
ff = lel.get_gata_dict('Tallinn')
pek = lel.get_data_by_city('Tokyo')
pf = lel.get_gata_dict('Tokyo')

