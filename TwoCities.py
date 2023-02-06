from flask import Flask
from flask_restful import Resource, Api
from datetime import datetime
import pytz


class TwoCities(Resource):
    def get(self, city1, city2):

        lines = []
        checker = 0

        with open('RU.txt', encoding='utf-8') as f:
            for line in f:
                if city1.capitalize() in line:
                    lines.append(line)
                    checker += 1
                    break

            for line in f:
                if city2.capitalize() in line:
                    lines.append(line)
                    checker += 1
                    break

            if checker != 2:
                return {'message': 'Two cities not found'}

        res = []
        temp = []
        cities = []

        for city in lines:
            cities.append({'city': city.split('\t')[1],
                           'latitude':   city.split('\t')[4],
                           'longitude':   city.split('\t')[5],
                           'timezone': city.split('\t')[17]
                           })

        if float(lines[0].split('\t')[4]) > float(lines[1].split('\t')[4]):
            temp.append(lines[0].split('\t')[1])
        elif float(lines[0].split('\t')[4]) < float(lines[1].split('\t')[4]):
            temp.append(lines[1].split('\t')[1])
        else:
            temp.append('same')

        if lines[0][17] == lines[1][17]:
            temp.append('same')
        else:
            firstTzOffset = pytz.timezone(
                lines[0].split('\t')[17]).utcoffset(datetime.now())
            secondTzOffset = pytz.timezone(
                lines[1].split('\t')[17]).utcoffset(datetime.now())

            temp.append(abs((secondTzOffset - firstTzOffset).seconds/3600))

        cities.append(
            {'northern': temp[0],
             'timezonediff': temp[1]
             })

        return cities
