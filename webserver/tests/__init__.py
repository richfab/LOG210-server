# Configuration of Flask application
from webserver import app
from webserver.config import TestingConfig
app.config.from_object(TestingConfig)

# Configure DataBase and create it
from webserver import db
db.initialize(app.config['SQLALCHEMY_DATABASE_URI'])
db.create_all()

# Import models
from webserver.models import Address, Client, Country, Dish, Entrepreneur, Livreur, LineOrder, Menu, Order, Personne, Restaurant, Restaurateur, StateOrder

# Import others
import datetime



# Builders and deleters
################################################


# Address
def build_address(id, address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", country=None, personne_id=None):
    """ Builder to create an address in database """

    if country is None:
        country = build_country(id=id)

    address = Address(id=id, address=address, zipcode=zipcode, city=city, country=country, personne_id=personne_id)
    db.session.add(address)

    return address

def delete_addresses():
    """ Remove all clients from database """

    for address in db.session.query(Address).all():
        db.session.delete(address)

    delete_countries()
    
    
# Client
def build_client(id, firstname="Toto", lastname="Bob", phone="444-444-4444", address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", mail="boby@resto.ca", password="azerty", birthdate=None, country=None):
    """ Builder to create a client in database """

    if birthdate is None:
        birthdate = datetime.datetime(2014, 4, 4)

    if country is None:
        country = build_country(id=id)

    client = Client(id=id, firstname=firstname, lastname=lastname, birthdate=birthdate, phone=phone, address=address, zipcode=zipcode, city=city, country=country, mail=mail, password=password)
    db.session.add(client)

    return client

def delete_clients():
    """ Remove all clients from database """

    for client in db.session.query(Client).all():
        db.session.delete(client)

    delete_countries()


# Country
def build_country(id, name="Canada"):
    """ Builder to create a country in database """

    country = Country(id=id, name=name)
    db.session.add(country)

    return country

def delete_countries():
    """ Remove all country from database """

    for country in db.session.query(Country).all():
        db.session.delete(country)


# Dish
def build_dish(id, name="Mega Burger", description="Un burger", price=14.32, menu_id=None):
    """ Builder to create a client in database """

    dish = Dish(id=id, name=name, description=description, price=price, menu_id=menu_id)
    db.session.add(dish)

    return dish

def delete_dishes():
    """ Remove all dishes from database """

    for dish in db.session.query(Dish).all():
        db.session.delete(dish)
        
        
# Entrepreneur
def build_entrepreneur(id, firstname="Toto", lastname="Bob", phone="444-444-4444", address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", mail="boby@resto.ca", password="azerty", birthdate=None, country=None):
    """ Builder to create an entrepreneur in database """

    if birthdate is None:
        birthdate = datetime.datetime(2014, 4, 4)

    if country is None:
        country = build_country(id=id)

    entrepreneur = Entrepreneur(id=id, firstname=firstname, lastname=lastname, birthdate=birthdate, phone=phone, address=address, zipcode=zipcode, city=city, country=country, mail=mail, password=password)
    db.session.add(entrepreneur)

    return entrepreneur

def delete_entrepreneurs():
    """ Remove all entrepreneurs from database """

    for entrepreneur in db.session.query(Entrepreneur).all():
        db.session.delete(entrepreneur)

    delete_countries()


# Livreur
def build_livreur(id, firstname="Toto", lastname="Bob", phone="444-444-4444", address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", mail="boby@resto.ca", password="azerty", birthdate=None, country=None):
    """ Builder to create a livreur in database """

    if birthdate is None:
        birthdate = datetime.datetime(2014, 4, 4)

    if country is None:
        country = build_country(id=id)

    livreur = Livreur(id=id, firstname=firstname, lastname=lastname, birthdate=birthdate, phone=phone, address=address, zipcode=zipcode, city=city, country=country, mail=mail, password=password)
    db.session.add(livreur)

    return livreur

def delete_livreurs():
    """ Remove all livreurs from database """

    for livreur in db.session.query(Livreur).all():
        db.session.delete(livreur)

    delete_countries()


# LineOrder
def build_line_order(id, order_id, dish_id=None, quantity=1):
    """ Builder to create a livreur in database """

    if dish_id is None:
        build_dish(id=id)
        dish_id=id

    line_order = LineOrder(id=id, dish_id=dish_id, quantity=quantity, order_id=order_id)
    db.session.add(line_order)

    return line_order

def delete_lines_order():
    """ Remove all line order from database """

    for lo in db.session.query(LineOrder).all():
        db.session.delete(lo)
        
    delete_dishes()


# Menu
def build_menu(id, name="Menu de printemps", restaurant_id=None):
    """ Builder to create a menu in database """

    menu = Menu(id=id, name=name, restaurant_id=restaurant_id)
    db.session.add(menu)

    return menu

def delete_menus():
    """ Remove all menus from database """

    for menu in db.session.query(Menu).all():
        db.session.delete(menu)


# Order
def build_order(id, number=1, date=None, client_id=None, restaurant_id=None, state=None):
    """ Builder to create a menu in database """

    date = datetime.datetime(2014, 4, 4) if date is None else date
    state = StateOrder(name="En attente") if state is None else state
    db.session.add(state)
    
    order = Order(id=id, number=number, date=date, client_id=client_id, restaurant_id=restaurant_id, state=state)
    db.session.add(order)

    return order

def delete_orders():
    """ Remove all menus from database """

    for order in db.session.query(Order).all():
        db.session.delete(order)
    
    delete_states_orders()  
             
        
# Personne
def build_personne(id, firstname="Toto", lastname="Bob", phone="444-444-4444", address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", mail="boby@resto.ca", password="azerty", birthdate=None, country=None):
    """ Builder to create a personne in database """

    if birthdate is None:
        birthdate = datetime.datetime(2014, 4, 4)

    if country is None:
        country = Country(name="Canada")

    personne = Personne(id=id, firstname=firstname, lastname=lastname, birthdate=birthdate, phone=phone, address=address, zipcode=zipcode, city=city, country=country, mail=mail, password=password)
    db.session.add(personne)

    return personne

def delete_personnes():
    """ Remove all personnes from database """

    for personne in db.session.query(Personne).all():
        db.session.delete(personne)

    delete_countries()

# Restaurateur
def build_restaurateur(id, firstname="Toto", lastname="Bob", phone="444-444-4444", address="1010 Avenue de la banquise", zipcode="H1S1R1", city="Montreal", mail="boby@resto.ca", password="azerty", birthdate=None, country=None):
    """ Builder to create a personne in database """

    if birthdate is None:
        birthdate = datetime.datetime(2014, 4, 4)

    if country is None:
        country = Country(name="Canada")

    restaurateur = Restaurateur(id=id, firstname=firstname, lastname=lastname, birthdate=birthdate, phone=phone, address=address, zipcode=zipcode, city=city, country=country, mail=mail, password=password)
    db.session.add(restaurateur)

    return restaurateur

def delete_restaurateurs():
    """ Remove all personnes from database """

    for restaurateur in db.session.query(Restaurateur).all():
        db.session.delete(restaurateur)

    delete_countries()


# Restaurant
def build_restaurant(id, name="Resto 1", phone="514-444-4444", cooking_type="Asian cooking", address="1010 Ste-Catherie", zipcode="H1S1R1", city="Montreal", country=None, restaurateur=None):
    """ Builder to create a restaurant in database """

    restaurant = Restaurant(id=id, name=name, phone=phone, cooking_type=cooking_type, address=address, zipcode=zipcode, city=city, country=country, restaurateur=restaurateur)
    db.session.add(restaurant)

    return restaurant

def delete_restaurants():
    """ Remove all restaurant from database """

    for restaurant in db.session.query(Restaurant).all():
        restaurant.restaurateur = None
        db.session.delete(restaurant)
        
# StateOrder
def build_state_order(id, name="Ready"):
    """ Builder to create a StateOrder in database """

    so = StateOrder(id=id, name=name)
    db.session.add(so)

    return so

def delete_states_orders():
    """ Remove all StateOrder from database """

    for so in db.session.query(StateOrder).all():
        db.session.delete(so)