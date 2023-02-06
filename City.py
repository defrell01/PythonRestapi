from flask import Flask
from flask_restful import Resource, Api


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
