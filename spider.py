# -*- coding:utf-8 -*-
#Author: uimeis

import requests
import json
import datetime

#必填API，请自行申请，http://openweathermap.org/
APP_KEY = ''

#输入城市名称
city = input('输入你的城市（必须英文）')

#请求API
def url_builder_name(city_name):
    api = 'http://api.openweathermap.org/data/2.5/weather?q='
    unit = 'metric'
    url = api + city_name + '&lang=zh_cn' + '&units=' + unit + '&APPID=' + APP_KEY
    res = requests.get(url)
    return json.loads(res.text)

a = url_builder_name(city)

#时间格式转换
def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%H:%M')
    return converted_time

#风速，参考https://baike.baidu.com/item/%E9%A3%8E%E9%80%9F/75302?fr=aladdin
wind = a.get('wind')['speed']
if wind>0.0 and wind<0.2:
    wind = 0
elif wind>=0.2 and wind<1.5:
    wind = 1
elif wind>=1.5 and wind<3.3:
    wind = 2
elif wind>=3.3 and wind<5.4:
    wind = 3
elif wind>=5.4 and wind<7.9:
    wind = 4
elif wind>=7.9 and wind<10.7:
    wind = 5
elif wind>=10.7 and wind<13.8:
    wind = 6
elif wind>=13.8 and wind<17.1:
    wind = 7
elif wind>=17.1 and wind<20.7:
    wind = 8
elif wind>=20.7 and wind<24.4:
    wind = 9
elif wind>=24.4 and wind<28.4:
    wind = 10
elif wind>=28.4 and wind<32.6:
    wind = 11
elif wind>=32.6 and wind<36.9:
    wind = 12

#风向，参考https://baike.baidu.com/item/%E9%A3%8E%E5%90%91/4869036?fr=aladdin
wind_deg = a.get('wind')['deg']
if wind_deg>22.5 and wind_deg<=67.5:
    wind_deg = '东北风'
elif wind_deg>67.5 and wind_deg<=112.5:
    wind_deg = '东风'
elif wind_deg>112.5 and wind_deg<=157.5:
    wind_deg = '东南风'
elif wind_deg>157.5 and wind_deg<=202.5:
    wind_deg = '南风'
elif wind_deg>202.5 and wind_deg<=247.5:
    wind_deg = '西南风'
elif wind_deg>247.5 and wind_deg<=292.5:
    wind_deg = '西风'
elif wind_deg>292.5 and wind_deg<=337.5:
    wind_deg = '西北风'
elif wind_deg>337.5 and wind_deg<=360 or wind_deg>0 and wind_deg<=22.5:
    wind_deg = '北风'

#提取数据，构建字典
def data_organizer(a):
    data = {
        'city': a.get('name'),
        'country': a.get('sys')['country'],
        'temp': a.get('main')['temp'],
        'temp_max': a.get('main')['temp_max'],
        'temp_min': a.get('main')['temp_min'],
        'humidity': a.get('main')['humidity'],
        'pressure': a.get('main')['pressure'],
        'sky': a.get('weather')[0]['main'],
        'sunrise': time_converter(a.get('sys')['sunrise']),
        'sunset': time_converter(a.get('sys')['sunset']),
        'wind': wind,
        'wind_deg': wind_deg,
        'dt': time_converter(a.get('dt')),
        'cloudiness': a.get('clouds')['all'],
        'description': a.get('weather')[0]['description']
    }
    return data

#输出格式
def data_output():
    s = '''
------------------------------------------------
    当前气温: {city}, {country}:{temp}°C {description}
    最高值: {temp_max}°C, 最低值: {temp_min}°C
    
    风速: {wind}级, 风向: {wind_deg}
    湿度: {humidity}%
    气压: {pressure}百帕（hPa）
    日出: {sunrise}
    日落: {sunset}
    
    最后更新时间: {dt}
------------------------------------------------'''
    return s.format(**data_organizer(a))

print(data_output())