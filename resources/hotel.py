from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3
from resources.filtros import normalize_path_params, Hoteis
from models.site import SiteModel

 

path_params=reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help='The field "nome" cannot be left blank')
    argumentos.add_argument('estrelas', type=float, required=True, help='The field "estrelas" cannot be left blank')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade') 
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site")  
    
    def get(self, hotel_id):
        hotel=HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 # not found

    @jwt_required()
    def post(self, hotel_id): 
        if HotelModel.find_hotel(hotel_id):
            return{'message': 'Hotel ID "{}" already exists.'.format(hotel_id)}, 400

        dados=Hotel.argumentos.parse_args()
        hotel=HotelModel(hotel_id, **dados)
        if not SiteModel.find_by_id(dados.get('site_id')):
            return {"message": "The hotel must be associated with a valid site id."}, 400
    
        try:       
            hotel.save_hotel()
        except:
            return{'message':'Database error.'}, 500
        return hotel.json()
        
    @jwt_required()
    def put(self, hotel_id):
        dados=Hotel.argumentos.parse_args()
        hotel_encontrado=HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel=HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return{'message':'Database error.'}, 500
        return hotel.json()

    @jwt_required()
    def delete(self, hotel_id):
        hotel=HotelModel.find_hotel(hotel_id)
        if hotel:
                hotel.delete_hotel()
                return{'message':'Hotel deleted.'}, 200
        return{'message': 'Hotel not found.'}, 404