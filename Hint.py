from flask import Flask
from flask_restful import Resource, Api


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
