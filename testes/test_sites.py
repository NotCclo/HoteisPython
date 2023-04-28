from conftest import *
from models.site import SiteModel


def t_add_site(siteurl, siteid, sitehoteis):
    site = SiteModel(siteurl)

    site.url = siteurl
    site.site_id = siteid
    site.hoteis = sitehoteis
    
    banco.session.add(site)
    banco.session.commit()

def t_delete_site(url):
    site = SiteModel.query.filter_by(url=url).first()
    if site:
        banco.session.delete(site)
        banco.session.commit()
    return 404

def t_delete_site2(url):
    site = SiteModel.query.filter_by(url=url).first()
    if site:
        banco.session.delete(site)
        banco.session.commit()

def t_delete_all_sites():
    for site in SiteModel.query.all():
        banco.session.delete(site)
        banco.session.commit()

def test_get_sites(client):
    
    with app.app_context():

        url_test = "www.teste.com"
        siteid_test = 1
        hoteis_test = []

        t_delete_all_sites()

        t_add_site (url_test, siteid_test, hoteis_test)

        url="/sites"


        response=client.get(url)
        print ("Hello World!")
        object=json.loads(response.data)
        sites=object["sites"]
        print (sites)
        #user=User.query.get(sites) 

        assert response.status_code == 200
        assert len(sites) == 1
        # assert data["login"] == user.login
        # assert data["senha"] == user.senha

        t_delete_site(url_test)


def test_get_site(client):

    with app.app_context():

        url_test = "www.teste.com"
        siteid_test = 2
        hoteis_test = []

        t_delete_all_sites()

        t_add_site (url_test, siteid_test, hoteis_test)

        url="/sites/" + url_test
    
        response=client.get(url)
        print ("Hello World!")
        object=json.loads(response.data)
        #sites=object["sites"]
        #print (sites)
        #user=User.query.get(sites) 

        assert response.status_code == 200
        assert object["site_id"] == siteid_test
        assert object["url"] == url_test
        assert object["hoteis"] == hoteis_test

        t_delete_site(url_test)

def test_post_site(client):

    with app.app_context():

        url_test = "www.teste.com"
        siteid_test = 2
        hoteis_test = []

        t_delete_all_sites()

        data= {
            "site_id": siteid_test,
            "url":  url_test,
            "hoteis": hoteis_test
        }

        url = "/sites/" + url_test

        response = client.post(url, data=json.dumps(data))
        object=json.loads(response.data)

        assert response.status_code == 200
        assert object["url"] == url_test
        assert object["hoteis"] == hoteis_test

        t_delete_site(url_test)

def test_del_site(client):

    with app.app_context():

        url_test = "www.teste.com"
        siteid_test = 90
        hoteis_test = []

        t_delete_all_sites()
        
        t_add_site (url_test, siteid_test, hoteis_test)

        url = "/sites/" + url_test

        response = client.delete(url)
        object=json.loads(response.data)
        site = SiteModel.query.filter_by(url=url_test).first()

        assert response.status_code == 200
        assert site == None