from conftest import *
from models.hotel import HotelModel
from test_sites import t_add_site, t_delete_site, t_delete_all_sites


def t_add_hotel(hotelid, hotelsiteid, hotelestrelas, hotelcidade, hoteldiaria, hotelnome):
    hotel = HotelModel(hotelid, hotelsiteid, hotelestrelas, hotelcidade, hoteldiaria, hotelnome)

    hotel.nome = hotelnome
    hotel.site_id = hotelsiteid
    hotel.estrelas = hotelestrelas
    hotel.diaria = hoteldiaria
    hotel.cidade = hotelcidade
    hotel.hotel_id = hotelid
    
    banco.session.add(hotel)
    banco.session.commit()

def t_delete_hotel(hotel_id):
    hotel = HotelModel.query.filter_by(hotel_id=hotel_id).first()
    if hotel:
        banco.session.delete(hotel)
        banco.session.commit()
    return 404 

def t_delete_all_hoteis():
    for hotel in HotelModel.query.all():
        banco.session.delete(hotel)
        banco.session.commit()

def test_get_hoteis(client):
    with app.app_context():

        url_test = "www.teste2.com"
        siteid_test = 2
        hoteis_test = []

        t_delete_all_hoteis()
        t_delete_all_sites()

        t_add_site (url_test, siteid_test, hoteis_test)

        hid_test = "teste"
        sid_test = 2
        est_test = 4.25
        cid_test = "Cuiabá"
        dia_test = 430.50
        nom_test = "Teste Hotel"

        t_add_hotel (hid_test, sid_test, est_test, cid_test, dia_test, nom_test)

        url = "/hoteis"

        response = client.get(url)
        object=json.loads(response.data)

        print (object)

        assert response.status_code == 200
        assert object["hoteis"][0]["estrelas"] == est_test
        assert object["hoteis"][0]["hotel_id"] == hid_test
        assert object["hoteis"][0]["site_id"] == sid_test
        assert object["hoteis"][0]["cidade"] == cid_test
        assert object["hoteis"][0]["diaria"] == dia_test
        assert object["hoteis"][0]["nome"] == nom_test

        t_delete_hotel(hid_test)
        t_delete_site(url_test)

def test_get_hotel(client):

    with app.app_context():

        url_test = "www.teste.com"
        siteid_test = 2
        hoteis_test = []

        t_delete_all_hoteis()
        t_delete_all_sites()

        t_add_site (url_test, siteid_test, hoteis_test)

        hid_test = "teste141"
        sid_test = 2
        est_test = 4
        cid_test = "BH"
        dia_test = 430
        nom_test = "Teste Hotellala"

        t_add_hotel (hid_test, sid_test, est_test, cid_test, dia_test, nom_test)

        url="/hoteis/" + hid_test
    
        response=client.get(url)
        print ("Hello World!")
        object=json.loads(response.data)

        assert response.status_code == 200
        assert object["estrelas"] == est_test
        assert object["hotel_id"] == hid_test
        assert object["site_id"] == sid_test
        assert object["cidade"] == cid_test
        assert object["diaria"] == dia_test
        assert object["nome"] == nom_test

        t_delete_site(url_test)
        t_delete_hotel(hid_test)

def test_post_hotel(client):

    with app.app_context():

        url_test = "www.teste.com"
        siteid_test = 2
        hoteis_test = []

        t_delete_all_hoteis()
        t_delete_all_sites()

        t_add_site (url_test, siteid_test, hoteis_test)

        hid_test = "teste"
        sid_test = 2
        est_test = 4
        cid_test = "BH"
        dia_test = 430
        nom_test = "Teste Hotel"

        data= {
            "hotel_id": hid_test,
            "nome":  nom_test,
            "estrelas": est_test,
            "diaria": dia_test,
            "cidade": cid_test,
            "site_id": sid_test
        }

        url = "/hoteis/" + hid_test

        access_token = get_access_token(client)

        response = client.post(url, data=json.dumps(data), headers=make_headers(access_token))
        object=json.loads(response.data)

        assert response.status_code == 200
        assert object["estrelas"] == est_test
        assert object["hotel_id"] == hid_test
        assert object["site_id"] == sid_test
        assert object["cidade"] == cid_test
        assert object["diaria"] == dia_test
        assert object["nome"] == nom_test

        t_delete_hotel(hid_test)
        t_delete_site(url_test)

def test_del_hotel(client):

    with app.app_context():

        url_test = "www.teste.com"
        siteid_test = 2
        hoteis_test = []

        t_delete_all_hoteis()
        t_delete_all_sites()

        t_add_site (url_test, siteid_test, hoteis_test)

        hid_test = "teste"
        sid_test = 2
        est_test = 4
        cid_test = "BH"
        dia_test = 430
        nom_test = "Teste Hotel"

        t_add_hotel (hid_test, sid_test, est_test, cid_test, dia_test, nom_test)


        url = "/hoteis/" + hid_test

        access_token = get_access_token(client)

        response = client.delete(url, headers=make_headers(access_token))
        hotel = HotelModel.query.filter_by(hotel_id=hid_test).first()
        print (response.data)

        assert response.status_code == 200
        assert hotel == None

def test_put_hotel(client):

    with app.app_context():

        url_test = "www.teste.com"
        siteid_test = 2
        hoteis_test = []

        t_delete_all_hoteis()
        t_delete_all_sites()

        t_add_site (url_test, siteid_test, hoteis_test)

        hid_test = "teste"
        sid_test = 2
        est_test = 4
        cid_test = "BH"
        dia_test = 430
        nom_test = "Teste Hotel"

        data= {
            "hotel_id": hid_test,
            "nome":  nom_test,
            "estrelas": est_test,
            "diaria": dia_test,
            "cidade": cid_test,
            "site_id": sid_test
        }

        url = "/hoteis/" + hid_test

        access_token = get_access_token(client)

        response = client.put(url, data=json.dumps(data), headers=make_headers(access_token))
        object=json.loads(response.data)

        assert response.status_code == 200
        assert object["estrelas"] == est_test
        assert object["hotel_id"] == hid_test
        assert object["site_id"] == sid_test
        assert object["cidade"] == cid_test
        assert object["diaria"] == dia_test
        assert object["nome"] == nom_test

        t_delete_hotel(hid_test)
        t_delete_site(url_test)