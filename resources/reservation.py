from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.client import ClientModel
from models.reservation import ReservationModel

clients=[
        {
        'client_id': 5, 
        'nome': 'Roberto'
        }
]
class Reservation(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('client_id')
    argumentos.add_argument('hotel_id')
    argumentos.add_argument('room_type')
    argumentos.add_argument('data_ini')
    argumentos.add_argument('data_end')

    def post(self):  
        dados=Reservation.argumentos.parse_args()

        if ClientModel.exists(clients, dados.client_id) and hotel.exists(dados.hotel_id):
            res_objeto=ReservationModel(**dados)
            novo_res= res_objeto.json()

            return novo_res, 200
        return {'message': 'Client or Hotel not found.'}, 404 # not found