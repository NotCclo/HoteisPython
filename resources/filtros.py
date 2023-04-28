from models.hotel import HotelModel
from flask_restful import Resource, reqparse

def normalize_path_params(cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=10000, limit=50, offset=0, **dados):
    if cidade:
        return{
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset}
    return{
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit': limit,
            'offset': offset}

path_params=reqparse.RequestParser()
path_params.add_argument('cidade', type=str, location="args")
path_params.add_argument('estrelas_min', type=float, location="args")
path_params.add_argument('estrelas_max', type=float, location="args")
path_params.add_argument('diaria_max', type=float, location="args")
path_params.add_argument('diaria_min', type=float, location="args")
path_params.add_argument('limit', type=float, location="args")
path_params.add_argument('offset', type=float, location="args")

class Hoteis(Resource):
    def get(self):


        q=HotelModel.query
        
        if path_params is not None:
            dados=path_params.parse_args()
            dados_validos={chave:dados[chave] for chave in dados if dados[chave] is not None}
            parametros = normalize_path_params(**dados_validos)

        #q=HotelModel.query

            if parametros.get('estrelas_min') is not None:
                q=q.filter(HotelModel.estrelas>=parametros.get('estrelas_min'))

            if parametros.get('estrelas_max') is not None:
                q=q.filter(HotelModel.estrelas<=parametros.get('estrelas_max'))

            if parametros.get('diaria_min') is not None:
                q=q.filter(HotelModel.diaria>=parametros.get('diaria_min'))

            if parametros.get('diaria_max') is not None:
                q=q.filter(HotelModel.diaria<=parametros.get('diaria_max'))

            if parametros.get('cidade') is not None:
                q=q.filter(HotelModel.cidade==parametros.get('cidade'))

            if parametros.get('limit') is not None:
                q=q.limit(parametros.get('limit'))

            if parametros.get('offset') is not None:
                q=q.offset(parametros.get('offset'))

        resultado=q.all()
        
        hoteis=[]
        for linha in resultado:
           
            hoteis.append({
            "hotel_id": linha.hotel_id,
            "nome": linha.nome,
            "estrelas": linha.estrelas,
            "diaria": linha.diaria,
            "cidade": linha.cidade,
            "site_id": linha.site_id
            })

        return {'hoteis': hoteis}

