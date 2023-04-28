from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        for site in SiteModel.query.all():
            print (site)
            print (site.json())
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        site=SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site not found'}, 404

    def post(self, url):
        if SiteModel.find_site(url):
            return {'message': 'This site already exists.'}, 400
        site = SiteModel(url)
        site.save_site()
        return site.json()

    def delete(self, url):
        site=SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'Site deleted.'}, 200
        return {'message': 'Site not found.'}, 404