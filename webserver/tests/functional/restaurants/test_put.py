from webserver import db
from webserver.models import Restaurant, Restaurateur
from webserver.tests import build_restaurant, build_restaurateur
from webserver.tests import delete_restaurants, delete_restaurateurs
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=5)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_exists(self):
        """ PUT /restaurants/id: exists """

        # Check request
        response = self.put('/restaurants/5')
        assert response.status_code != 404
        assert response.status_code != 500


class UnknownParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=1)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_unkown_id(self):
        """ PUT /restaurants/id: with unkown id """

        # Check request
        response = self.put('/restaurants/5')
        assert response.status_code == 400
        assert response.data == 'Le restaurant n\'existe pas.'

    def test_unkown_restaurateur_id(self):
        """ PUT /restaurants/id: with unkown restaurateur id """

        data = dict()
        data['restaurateur_id'] = 100

        # Check request
        response = self.put('/restaurants/1', data=data)
        assert response.status_code == 404
        assert response.data == 'Le restaurateur n\'existe pas.'


class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_restaurant(id=5, name="Resto 1")
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        db.session.commit()

    def test_invalid_name(self):
        """ PUT /restaurants/id: with invalid name """

        # Prepare data
        data = dict()
        data['name'] = 1

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom doit etre une chaine de caractere.'

    def test_invalid_address(self):
        """ PUT /restaurants/id: with invalid address """

        # Prepare data
        data = dict()
        data['address'] = 14029

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 400
        assert response.data == 'L\'adresse doit etre une chaine de caractere.'

    def test_invalid_city(self):
        """ PUT /restaurants/id: with invalid city """

        # Prepare data
        data = dict()
        data['city'] = 1

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 400
        assert response.data == 'La ville doit etre une chaine de caractere.'

    def test_invalid_phone(self):
        """ PUT /restaurants/id: with invalid phone """

        # Prepare data
        data = dict()
        data['phone'] = 3422.2

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 400
        assert response.data == 'Le numero de telephone doit etre une chaine de caractere.'


class Update(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        r1 = build_restaurateur(id=10)
        r2 = build_restaurateur(id=15)
        r3 = build_restaurateur(id=20)
        r4 = build_restaurateur(id=25)

        build_restaurant(id=5, name="La banquise", restaurateur=r1)
        build_restaurant(id=7, name="Le tigre rouge", restaurateur=r3)
        build_restaurant(id=9, name="Le lion du sud", restaurateur=r4)
        build_restaurant(id=11, name="Le lion du sud")

        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_restaurants()
        delete_restaurateurs()
        db.session.commit()

    def test_update(self):
        """ PUT /restaurants/id: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Le duc de Lorraine"
        data['phone'] = "514-555-5555"
        data['address'] = "9000 Boulevard de Carrie"
        data['city'] = "Trois-Rivieres"
        data['restaurateur_id'] = 15

        # Check request
        response = self.put('/restaurants/5', data=data)
        assert response.status_code == 200

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurant = db.session.query(Restaurant).get(result['id'])
        assert restaurant.name == 'Le duc de Lorraine'
        assert restaurant.phone == "514-555-5555"
        assert restaurant.address == '9000 Boulevard de Carrie'
        assert restaurant.city == 'Trois-Rivieres'
        assert restaurant.restaurateur.id == 15

        # Check restaurant in restaurateur
        restaurateur = db.session.query(Restaurateur).get(15)
        assert restaurateur.restaurant.id == result['id']

    def test_update_without_restaurateur(self):
        """ PUT /restaurants/id: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "La banquise"
        data['phone'] = "514-555-5555"
        data['address'] = "9000 Boulevard de Carrie"
        data['city'] = "Trois-Rivieres"

        # Check request
        response = self.put('/restaurants/7', data=data)
        assert response.status_code == 200

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        restaurant = db.session.query(Restaurant).get(result['id'])
        assert restaurant.name == 'La banquise'
        assert restaurant.phone == "514-555-5555"
        assert restaurant.address == '9000 Boulevard de Carrie'
        assert restaurant.city == 'Trois-Rivieres'
        assert restaurant.restaurateur is None

        # Check restaurant in restaurateur
        restaurateur = db.session.query(Restaurateur).get(20)
        assert restaurateur.restaurant is None


    def test_update_with_restaurateur_already_assigned(self):
        """ PUT /restaurants/id: with valid data """

        # Prepare data
        data = dict()
        data['restaurateur_id'] = 25

        # Check request
        response = self.put('/restaurants/11', data=data)
        assert response.status_code == 400
        assert response.data == 'Le restaurateur est deja assignee a un restaurant.'