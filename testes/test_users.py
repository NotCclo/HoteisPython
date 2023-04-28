from conftest import *
from models.usuario import UserModel

def t_add_user(userid, login, senha):
    user = UserModel(login, senha)

    user.user_id = userid
    user.login = login
    user.senha = senha
    
    banco.session.add(user)
    banco.session.commit()

def t_delete_user(login):
    user = UserModel.query.filter_by(login=login).first()
    if user:
        banco.session.delete(user)
        banco.session.commit()
    return 404 

def test_get_user(client):

    with app.app_context():

        uid_test = 1
        login_test = "zedapadoca"
        senha_test = "teste95"

        t_add_user (uid_test, login_test, senha_test)

        url="/usuarios/"+str(uid_test)
    
        response=client.get(url)
        print ("Hello World!")
        object=json.loads(response.data)

        assert response.status_code == 200
        assert object["user_id"] == uid_test
        assert object["login"] == login_test

        t_delete_user(login_test)

def test_del_user(client):

    with app.app_context():

        uid_test = "1"
        login_test = "zedapadoca"
        senha_test = "teste95"

        t_add_user (uid_test, login_test, senha_test)

        url = "/usuarios/" + uid_test

        access_token = get_access_token(client)

        response = client.delete(url, headers=make_headers(access_token))
        user = UserModel.query.filter_by(login=login_test).first()

        assert response.status_code == 200
        assert user == None
        
def test_cadastro(client):
   
    with app.app_context():

        uid_test = "1"
        login_test = "zedapadoca"
        senha_test = "teste95"

        url = "/cadastro"

        data= {
        "login": login_test,
        "senha": senha_test
        }

        response = client.post(url, data=json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            })
        print (response.data)
        user = UserModel.query.filter_by(login=login_test).first()

        assert response.status_code == 200
        assert user is not None

        t_delete_user(login_test)

def test_login(client):

    with app.app_context():

        url = "/login"
        data = {
        "login": "demo",
        "senha": "demo"
        }

        response = client.post(url, data=json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            })
        object=json.loads(response.data)
        
        assert response.status_code==200
        assert object["access_token"] is not None

def test_logout(client):

    with app.app_context():

        url = "/login"
        data = {
        "login": "demo",
        "senha": "demo"
        }

        client.post(url, data=json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            })
        
        url2 = "/logout"

        access_token = get_access_token(client)

        response = client.post(url2, data=json.dumps(data), headers=make_headers(access_token))
        print (response.data)
        object=json.loads(response.data)

        assert response.status_code == 200
        assert object["message"] == "Logged out succesfully!" 