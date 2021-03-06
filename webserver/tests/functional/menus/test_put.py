# -*- coding: utf-8 -*-

from webserver import db
from webserver.models import Menu
from webserver.tests import build_menu
from webserver.tests import delete_menus
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        db.session.commit()

    def test_exists(self):
        """ PUT /menus/id: exists """

        # Check request
        response = self.put('/menus/5')
        assert response.status_code != 404
        assert response.status_code != 500


class UnknownParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=15)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        db.session.commit()

    def test_unkown_id(self):
        """ PUT /menus/id: with unkown id """

        # Check request
        response = self.put('/menus/5')
        assert response.status_code == 404
        assert response.data == "Le menu n'existe pas."

    
class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        db.session.commit()

    def test_invalid_name(self):
        """ PUT /menus/id: with invalid name """

        # Prepare data
        data = dict()
        data['name'] = 1111

        # Check request
        response = self.put('/menus/5', data=data)
        assert response.status_code == 400
        assert response.data == "Le nom du menu doit être une chaine de caractère."


class Update(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_menu(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_menus()
        db.session.commit()

    def test_update(self):
        """ PUT /menus/id: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Menu des 4 saisons"   

        # Check request
        response = self.put('/menus/5', data=data)
        assert response.status_code == 200

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        menu = db.session.query(Menu).get(result['id'])
        assert menu.name == "Menu des 4 saisons"