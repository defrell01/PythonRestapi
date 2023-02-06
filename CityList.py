from flask import Flask
from flask_restful import Resource, Api


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
