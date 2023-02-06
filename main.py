import json
from datetime import datetime
import pytz
from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello World'}


class City(Resource):
    def get(self, geonameid):
        found = False
        with open('RU.txt', encoding='utf-8') as f:
            for line in f:
                if geonameid in line:
                    city = line
                    found = True
                    break
            if found:
                return {'city': city.split('\t')[1],
                        'latitude':   city.split('\t')[4],
                        'longitude':   city.split('\t')[5],
                        'timezone': city.split('\t')[17]
                        }
            else:
                return {'message': 'Geonameid not found'}


class CityList(Resource):
    def get(self, page, number):
        with open('RU.txt', encoding='utf-8') as f:
            lines = f.readlines()

        lines = lines[:56*page]

        lines = lines[:number]

        cities = []

        for city in lines:
            cities.append({'city': city.split('\t')[1],
                           'latitude':   city.split('\t')[4],
                           'longitude':   city.split('\t')[5],
                           'timezone': city.split('\t')[17]
                           })

        return cities


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


class Hint(Resource):
    def get(self, name):
        names = []

        with open('RU.txt', encoding='utf-8') as f:
            for line in f:
                if line.split('\t')[1].lower().startswith(name.lower()):
                    names.append(line.split('\t')[1])
        names = list(set(names))

        if not names:
            return {'message': 'Name not found'}

        else:
            res = []
            for city in names:
                res.append({'hint': city})

            return res


api.add_resource(HelloWorld, '/api/hello')
api.add_resource(City, '/api/city/<string:geonameid>')
api.add_resource(CityList, '/api/citylist/<int:page>/<int:number>')
api.add_resource(TwoCities, '/api/cities/<string:city1>/<string:city2>')
api.add_resource(Hint, '/api/hint/<string:name>')


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='127.0.0.1')
