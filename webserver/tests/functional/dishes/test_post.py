from webserver import db
from webserver.models import Dish
from webserver.tests import build_dish
from webserver.tests import delete_dishes
from webserver.tests.functional import FunctionalTest


class Exists(FunctionalTest):
    """ Check if the webservice exists """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_exists(self):
        """ POST /dishes: exists """

        # Check request
        response = self.post('/dishes')
        assert response.status_code != 404
        assert response.status_code != 500


class MissingParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass

    def test_missing_name(self):
        """ POST /dishes: with missing name """

        # Prepare data
        data = dict()
        data['description'] = "un bon burger"
        data['price'] = 111.11

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom du plat est obligatoire.'

    def test_missing_description(self):
        """ POST /dishes: with missing description """

        # Prepare data
        data = dict()
        data['name'] = "Burger"
        data['price'] = 111.11

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'La description du plat est obligatoire.'

    def test_missing_price(self):
        """ POST /dishes: with missing price """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi"
       

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le price du plat est obligatoire.'

    
class InvalidParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        build_dish(id=10, price=222.22)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        db.session.commit()

    def test_invalid_name(self):
        """ POST /dishes: with invalid name """

        # Prepare data
        data = dict()
        data['name'] = 19090
        data['description'] = "Titi"
        data['price'] = 12.43

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le nom du plat doit etre une chaine de caractere.'


    def test_invalid_description(self):
        """ POST /dishes: with invalid description """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = 30923
        data['price'] = 12.43

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'La description du plat doit etre une chaine de caractere.'

    
    def test_invalid_price(self):
        """ POST /dishes: with invalid price """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi"
        data['price'] = "azerty"

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le price du plat doit etre numerique.'

    def test_negative_price(self):
        """ POST /dishes: with negative price """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi"
        data['price'] = (-30)

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 400
        assert response.data == 'Le price du plat doit etre positif.'


class UnknownParameters(FunctionalTest):
    """ Check with no datas """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        pass


class Create(FunctionalTest):
    """ Check with valid data """

    @classmethod
    def setup_class(cls):
        """ Add database fixtures """

        pass

    @classmethod
    def teardown_class(cls):
        """ Clear database fixtures """

        delete_dishes()
        db.session.commit()

    def test_create(self):
        """ POST /dishes: with valid data """

        # Prepare data
        data = dict()
        data['name'] = "Toto"
        data['description'] = "Titi description"
        data['price'] = 23.33

        # Check request
        response = self.post('/dishes', data=data)
        assert response.status_code == 201

        # Check received data
        result = self.parse(response.data)
        assert 'id' in result

        # Check in database
        dish = db.session.query(Dish).get(result['id'])
        assert dish is not None