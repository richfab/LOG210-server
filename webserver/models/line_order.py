from webserver.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

class LineOrder(Base):
    __tablename__ = 'line_order'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    
    dish_id = Column(Integer, ForeignKey('dish.id'))
    dish = relationship("Dish") 
    
    order_id = Column(Integer, ForeignKey('order.id'))
    
    def to_dict(self, dishes=True):
        my_dict = dict()

        my_dict['id'] = self.id
        my_dict['dish'] = self.dish.to_dict()
        my_dict['quantity'] = self.quantity
        
        return my_dict