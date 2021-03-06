from webserver.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)
    zipcode = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country")
    
    personne_id = Column(Integer, ForeignKey('personne.id'))

    def to_dict(self):
        my_dict = dict()
        
        my_dict['id'] = self.id
        my_dict['address'] = self.address
        my_dict['zipcode'] = self.zipcode
        my_dict['city'] = self.city

        if self.country:
            my_dict['country_id'] = self.country_id
            my_dict['country'] = self.country.to_dict()

        return my_dict