from flask import Flask
from flask_restful import Resource, Api
from City import City
from CityList import CityList
from TwoCities import TwoCities
from Hint import Hint


app = Flask(__name__)
api = Api(app)


api.add_resource(City, '/api/city/<string:geonameid>')
api.add_resource(CityList, '/api/citylist/<int:page>/<int:number>')
api.add_resource(TwoCities, '/api/cities/<string:city1>/<string:city2>')
api.add_resource(Hint, '/api/hint/<string:name>')


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='127.0.0.1')
