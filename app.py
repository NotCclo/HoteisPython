from flask import Flask, jsonify
from flask_restful import Api
from resources.site import Site, Sites
from resources.filtros import Hoteis
from resources.hotel import Hotel
from sql_alchemy import banco
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST 
from datetime import timedelta



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:MARsg%4099@localhost:5432/api_hoteis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY']='DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(days=30)
jwt = JWTManager(app)
banco.init_app(app)
api=Api(app)

with app.app_context():
    banco.create_all()

#@app.before_first_request
#def cria_banco():
#    banco.create_all

@jwt.token_in_blocklist_loader 
def verifica_blacklist(jwt_header, jwt_data):
    return jwt_data['jti'] in BLACKLIST 
    
@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_data):
    return jsonify({'message': 'You are not logged in.'}), 401 #unauthorized

api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')



if __name__ == '__main__':
    from sql_alchemy import banco
    #banco.init_app(app)
    app.run(debug=True)

