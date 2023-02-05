import json
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
    def get(self, page):
        with open('RU.txt', encoding='utf-8') as f:
            lines = f.readlines()
        lines = ''.join(lines[56*page])

        
        print(lines)




api.add_resource(HelloWorld, '/api/hello')
api.add_resource(City, '/api/city/<string:geonameid>')
api.add_resource(CityList, '/api/citylist/<int:page>/')

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='127.0.0.1')
